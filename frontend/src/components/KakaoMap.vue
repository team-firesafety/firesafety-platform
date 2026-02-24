<template>
  <div class="map-wrapper">
    <div ref="map" class="map"></div>

    <!-- ▸ 범례 -->
    <aside class="legend">
      <h4>🔥 화재 취약도</h4>
      <ul>
        <li
            v-for="bin in bins"
            :key="bin.color"
            :class="{ off: !shownColors.includes(bin.color) }"
            @click="toggleColor(bin.color)"
        >
          <span class="dot" :style="{ background: bin.color }"></span>
          <span class="txt">{{ bin.label }}</span>
          <span class="score">{{ bin.range }}</span>
        </li>
      </ul>
    </aside>
  </div>
</template>

<script>
import {loadKakao} from '@/utils/loadKakao.js';
import fireIcon from '@/assets/fire-station.png';

/* ─────────────────────────────────────────
   1. 하드코딩으로 추가할 두 건물
   ───────────────────────────────────────── */
const EXTRA_BUILDINGS = [
  {
    name: '그랑서울 (Gran Seoul)',
    lat: 37.5709617749066,
    lon: 126.981437983842,
    strctCdNm: '철골·철근콘크리트',
    riskScore: 7, // 낮음
    grndFloors: 24,
    bsmFloors: 7,
    totArea: 175_537,
    useAprDay: '2014-02-14'
  },
  {
    name: '동신빌딩',
    lat: 37.5767281582171,
    lon: 126.985404633757,
    strctCdNm: '철근콘크리트조',
    riskScore: 52, // 높음
    customColor: '#FF9E69', // 높음 색상 강제 지정
    grndFloors: 6,
    bsmFloors: 1,
    totArea: 1_000,
    useAprDay: '1970-11-25'
  }
];

/* ─────────────────────────────────────────
   2. 전역 상수
   ───────────────────────────────────────── */
const DOT = 20;
const R = 7;
const STATION_DOT = 48;

export default {
  name: 'KakaoMap',
  props: {
    buildings: {type: Array, required: true}, // 기존 건물 목록
    station: {type: Object, required: true}   // 소방서 정보
  },

  data() {
    return {
      kakao: null,
      map: null,
      allBuildings: [],      // 기존 + 추가 건물
      markers: [],
      clusterer: null,
      bins: [],
      shownColors: [],
      openOverlay: null
    };
  },

  async mounted() {
    this.kakao = await loadKakao();
    /* 기존 데이터와 EXTRA_BUILDINGS 합치기 */
    this.allBuildings = [...this.buildings, ...EXTRA_BUILDINGS];
    await this.init();
  },

  methods: {
    /* ───────── 초기화 ───────── */
    async init() {
      const center = await this.resolveStationPos();
      this.createMap(center);
      this.prepareBins();
      this.drawMarkers();
      this.drawStation(center);
      this.installClusterer();
    },

    /* ───────── 소방서 좌표 결정 ───────── */
    resolveStationPos() {
      const {kakao, station} = this;
      return new Promise(resolve => {
        if (station.addr) {
          const g = new kakao.maps.services.Geocoder();
          g.addressSearch(station.addr, (res, status) => {
            if (status === kakao.maps.services.Status.OK)
              return resolve(new kakao.maps.LatLng(res[0].y, res[0].x));
            resolve(new kakao.maps.LatLng(station.lat, station.lon));
          });
        } else {
          resolve(new kakao.maps.LatLng(station.lat, station.lon));
        }
      });
    },

    /* ───────── 지도 + dim ───────── */
    createMap(center) {
      this.map = new this.kakao.maps.Map(this.$refs.map, {center, level: 3});
      this.kakao.maps.event.addListener(this.map, 'tilesloaded', () => this.addDarkOverlay());
    },
    addDarkOverlay() {
      const node = this.map.getNode();
      
      // 카카오맵의 실제 DOM 구조 디버깅
      console.log('🔍 카카오맵 DOM 구조:');
      console.log('메인 노드:', node);
      console.log('자식 요소들:', [...node.children].map((child, index) => ({
        index,
        tag: child.tagName,
        classes: child.className,
        style: child.style.cssText,
        zIndex: getComputedStyle(child).zIndex
      })));
      
      // 지도 타일만 어둡게 하는 정확한 타겟팅
      const mapContainer = node.querySelector('div[style*="position: absolute"][style*="left: 0px"][style*="top: 0px"]');
      
      if (mapContainer) {
        console.log('🎯 지도 컨테이너 발견:', mapContainer);
        console.log('지도 컨테이너 자식들:', [...mapContainer.children].map((child, index) => ({
          index,
          tag: child.tagName,
          zIndex: getComputedStyle(child).zIndex || child.style.zIndex,
          hasImages: child.querySelectorAll('img').length
        })));
        
        // 실제 지도 타일이 있는 최하위 레이어에만 필터 적용
        const tileLayer = mapContainer.querySelector('div[style*="z-index: 0"]') || 
                         mapContainer.querySelector('div[style*="z-index: 1"]:first-child');
        
        if (tileLayer) {
          console.log('🗺️ 타일 레이어 발견:', tileLayer);
          tileLayer.style.filter = 'brightness(0.7)'; // 지도 타일만 어둡게
          console.log('✅ 지도 타일에 brightness 필터 적용');
        }
      }
    },

    /* ───────── 위험도 구간(50/80/95%) ───────── */
    prepareBins() {
      const xs = this.allBuildings.map(b => b.riskScore).sort((a, b) => a - b);
      const cut = p => xs[Math.min(xs.length - 1, Math.floor(xs.length * p))];
      const [c50, c80, c95] = [cut(.5), cut(.8), cut(.95)];

      const palette = ['#81E3B8', '#FFDB7C', '#FF9E69', '#FF6666'];
      const labels = ['낮음', '보통', '높음', '위험'];

      this.bins = [
        {min: -Infinity, max: c50, color: palette[0], label: labels[0], range: `≤ ${c50}`},
        {min: c50, max: c80, color: palette[1], label: labels[1], range: `${c50 + 1}~${c80}`},
        {min: c80, max: c95, color: palette[2], label: labels[2], range: ''},
        {min: c95, max: Infinity, color: palette[3], label: labels[3], range: ''}
      ];
      this.shownColors = this.bins.map(b => b.color);
    },
    colorOf(score) {
      return this.bins.find(b => score > b.min && score <= b.max).color;
    },

    /* ───────── 마커 & InfoWindow ───────── */
    drawMarkers() {
      const {kakao} = this;
      this.allBuildings.forEach(b => {
        const color = b.customColor || this.colorOf(b.riskScore);

        const marker = new kakao.maps.Marker({
          position: new kakao.maps.LatLng(b.lat, b.lon),
          image: this.makeDot(color),
          zIndex: 10
        });
        marker.setMap(this.map);

        const box = document.createElement('div');
        box.className = 'infow';
        box.style.setProperty('--infow-color', color);
        box.innerHTML = this.buildInfoHTML(b);

        const ov = new kakao.maps.CustomOverlay({
          position: marker.getPosition(),
          yAnchor: 1.05,
          zIndex: 20,
          content: box
        });
        this.markers.push({marker, color, ov});

        kakao.maps.event.addListener(marker, 'click', () => {
          if (this.openOverlay === ov) {
            ov.setMap(null);
            this.openOverlay = null;
          } else {
            this.openOverlay?.setMap(null);
            ov.setMap(this.map);
            this.openOverlay = ov;
          }
        });

        box.querySelector('.infow-close').addEventListener('click', e => {
          e.stopPropagation();
          ov.setMap(null);
          if (this.openOverlay === ov) this.openOverlay = null;
        });
      });
    },

    buildInfoHTML(b) {
      return `
        <button class="infow-close" aria-label="닫기">×</button>
        <h5>${b.name}</h5>
        <ul class="info-list">
          <li><span class="key">구조</span><span>${b.strctCdNm}</span></li>
          <li><span class="key">취약도</span><span>${b.riskScore}</span></li>
          <li><span class="key">층수</span><span>지상 ${b.grndFloors}F / 지하 ${b.bsmFloors}F</span></li>
          <li><span class="key">연면적</span><span>${b.totArea.toLocaleString()} ㎡</span></li>
          <li><span class="key">준공</span><span>${b.useAprDay}</span></li>
        </ul>`;
    },

    /* ───────── 소방서 마커 ───────── */
    drawStation(latlng) {
      new this.kakao.maps.Marker({
        position: latlng,
        title: this.station.name,
        image: new this.kakao.maps.MarkerImage(
            fireIcon,
            new this.kakao.maps.Size(STATION_DOT, STATION_DOT),
            {offset: new this.kakao.maps.Point(STATION_DOT / 2, STATION_DOT)}
        ),
        zIndex: 30
      }).setMap(this.map);
    },

    /* ───────── 클러스터 ───────── */
    installClusterer() {
      // MarkerClusterer 사용 가능 여부 확인
      if (this.kakao.maps.MarkerClusterer) {
        try {
          this.clusterer = new this.kakao.maps.MarkerClusterer({
            map: this.map,
            markers: this.markers.map(m => m.marker),
            minLevel: 6,
            averageCenter: true
          });
        } catch (error) {
          console.warn('MarkerClusterer 생성 실패:', error);
          this.clusterer = null;
        }
      } else {
        console.warn('MarkerClusterer를 사용할 수 없습니다.');
        this.clusterer = null;
      }
    },

    /* ───────── 점 마커 이미지 ───────── */
    makeDot(color) {
      const cv = document.createElement('canvas');
      cv.width = cv.height = DOT;
      const ctx = cv.getContext('2d');
      
      // 부드러운 그림자
      ctx.shadowColor = 'rgba(0,0,0,0.3)';
      ctx.shadowBlur = 4;
      
      // 투명도가 있는 마커 색상 (외곽선 제거)
      ctx.globalAlpha = 0.85; // 85% 불투명도 (15% 투명)
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(DOT / 2, DOT / 2, R, 0, Math.PI * 2);
      ctx.fill();
      
      return new this.kakao.maps.MarkerImage(
          cv.toDataURL(),
          new this.kakao.maps.Size(DOT, DOT),
          {offset: new this.kakao.maps.Point(DOT / 2, DOT / 2)}
      );
    },

    /* ───────── 범례 토글 ───────── */
    toggleColor(c) {
      const i = this.shownColors.indexOf(c);
      i === -1 ? this.shownColors.push(c) : this.shownColors.splice(i, 1);
      this.markers.forEach(({marker, color}) =>
          marker.setVisible(this.shownColors.includes(color))
      );
      if (this.clusterer) {
        this.clusterer.redraw();
      }
    }
  }
};
</script>

<!-- InfoWindow (전역) -->
<style>
:root {
  --infow-color: #4caf50;
}

/* Lint 통과용 기본값 */

.infow {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25);
  padding: 14px 16px 12px;
  width: 240px;
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  line-height: 1.55;
  position: relative;
  border-top: 4px solid var(--infow-color, #4caf50);
}

.infow h5 {
  margin: 0 0 10px;
  font-size: 15px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.infow .info-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  row-gap: 4px;
}

.infow .info-list .key {
  display: inline-block;
  width: 58px;
  font-weight: 600;
}

.infow-close {
  position: absolute;
  top: 6px;
  right: 8px;
  border: none;
  background: none;
  padding: 0;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
  opacity: 0.5;
  transition: 0.2s;
}

.infow-close:hover {
  opacity: 0.9;
}
</style>

<!-- 지도·범례 (scoped) -->
<style scoped>
.map-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.map {
  width: 100%;
  height: 100%;
}

.legend {
  position: absolute;
  right: 20px;
  bottom: 20px;
  z-index: 50;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  border-radius: 10px;
  padding: 12px 16px;
  font-size: 13px;
  min-width: 165px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend h4 {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 600;
}

.legend ul {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.legend li {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: 0.2s;
}

.legend li.off {
  opacity: 0.25;
}

.legend .dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
}

.legend .txt {
  flex: 0 0 40px;
}

.legend .score {
  display: none; /* 숫자 숨김 */
}
</style>
