<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="loading-container">
        <Loading />
        <p class="loading-text">생성중...</p>
      </div>

      <!-- 컬럼 선택 단계 -->
      <div v-else-if="!isChartGenerated" class="column-selection">
        <!-- 정보 버튼 -->
        <button 
          class="info-button" 
          @mouseenter="showTooltip = true" 
          @mouseleave="showTooltip = false"
        >
          i
        </button>

        <!-- 툴팁 -->
        <div v-if="showTooltip" class="tooltip">
          X축은 1개만 선택 가능하고, Y축은 최대 2개까지 선택 가능합니다.<br>
          Y축을 2개 선택하면 듀얼 Y축 그래프로 표시됩니다!
        </div>

        <h2 class="selection-title">데이터를 선택해주세요!</h2>
        
        <div class="axis-selection-container">
          <!-- X축 선택 -->
          <div class="axis-section">
            <h3 class="axis-title">X축 (1개 선택)</h3>
            <div class="checkbox-grid">
              <div 
                v-for="column in availableColumns" 
                :key="'x-' + column"
                class="checkbox-item"
                :class="{ selected: selectedXColumn === column }"
                @click="selectXColumn(column)"
              >
                <input 
                  type="checkbox" 
                  :checked="selectedXColumn === column"
                  @click="selectXColumn(column)"
                  @change.prevent
                />
                <span class="checkbox-label">{{ column }}</span>
              </div>
            </div>
          </div>

          <!-- Y축 선택 -->
          <div class="axis-section">
            <h3 class="axis-title">Y축 (최대 2개 선택)</h3>
            <div class="checkbox-grid">
              <div 
                v-for="column in numericColumns" 
                :key="'y-' + column"
                class="checkbox-item"
                :class="{ selected: selectedYColumns.includes(column) }"
                @click="selectYColumn(column)"
              >
                <input 
                  type="checkbox" 
                  :checked="selectedYColumns.includes(column)"
                  @click="selectYColumn(column)"
                  @change.prevent
                />
                <span class="checkbox-label">{{ column }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 선택 버튼 -->
        <button 
          class="select-button" 
          :disabled="!canGenerateChart"
          @click="generateChart"
        >
          선택
        </button>

        <!-- 최대 선택 알림 -->
        <div v-if="showMaxYAlert" class="max-y-alert">
          Y축은 최대 2개까지 선택 가능합니다!
        </div>
      </div>

      <!-- 차트 결과 -->
      <div v-else class="chart-result">
        <!-- 정보 버튼 -->
        <button 
          class="info-button" 
          @mouseenter="showChartTooltip = true" 
          @mouseleave="showChartTooltip = false"
        >
          i
        </button>

        <!-- 차트 툴팁 -->
        <div v-if="showChartTooltip" class="tooltip">
          첫번째 선택한 데이터가 x축이고, 두번째, 세번째 선택한 데이터가 y축으로 그래프상에 표시됩니다.<br>
          +버튼으로 그래프를 두개까지 만들어서 볼 수 있습니다!
        </div>

        <h2 class="chart-title">{{ chartTitle }}</h2>
        
        <!-- 차트 컨테이너 -->
        <div class="chart-container">
          <canvas ref="chartCanvas"></canvas>
        </div>

        <!-- 구분선 -->
        <div class="divider"></div>

        <!-- 범례 및 컬럼 재선택 통합 영역 -->
        <div class="legend-and-reselection">
          <!-- 범례 섹션 -->
          <div class="legend-section">
            <div class="legend-controls">
              <div 
                v-for="(dataset, index) in chartDatasets" 
                :key="'legend-' + index"
                class="legend-item"
              >
                <span 
                  class="legend-color" 
                  :style="{ backgroundColor: dataset.borderColor }"
                ></span>
                <span class="legend-label">{{ dataset.label }}</span>
              </div>
            </div>
          </div>

          <!-- 컬럼 재선택 영역 -->
          <div class="column-reselection">
            <div class="reselection-section">
              <h4 class="reselection-title">X축</h4>
              <div class="reselection-checkboxes">
                <div 
                  v-for="column in availableColumns" 
                  :key="'chart-x-' + column"
                  class="reselection-checkbox-item"
                  @click="selectXColumn(column); updateChart()"
                >
                  <input 
                    type="checkbox" 
                    :checked="selectedXColumn === column"
                    @click.stop="selectXColumn(column); updateChart()"
                    @change.prevent
                  />
                  <span class="reselection-checkbox-label">{{ column }}</span>
                </div>
              </div>
            </div>
            
            <div class="reselection-section">
              <h4 class="reselection-title">Y축</h4>
              <div class="reselection-checkboxes">
                <div 
                  v-for="column in numericColumns" 
                  :key="'chart-y-' + column"
                  class="reselection-checkbox-item"
                  @click="selectYColumn(column); updateChart()"
                >
                  <input 
                    type="checkbox" 
                    :checked="selectedYColumns.includes(column)"
                    @click.stop="selectYColumn(column); updateChart()"
                    @change.prevent
                  />
                  <span class="reselection-checkbox-label">{{ column }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 최대 선택 알림 (차트 화면용) -->
        <div v-if="showMaxYAlert" class="max-y-alert">
          Y축은 최대 2개까지 선택 가능합니다!
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Loading from './Loading.vue';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  Title,
  Tooltip,
  Legend
);

export default {
  name: 'ModalVis',
  components: { Loading },
  props: {
    data: { type: Object, required: true }
  },
  
  data() {
    return {
      isLoading: true,
      isChartGenerated: false,
      showTooltip: false,
      showChartTooltip: false,
      showMaxYAlert: false,
      
      availableColumns: [],
      numericColumns: [],
      selectedXColumn: null,
      selectedYColumns: [],
      
      chartInstance: null,
      chartDatasets: [],
      chartTitle: '',
      
      maxYAlertTimeout: null
    };
  },
  
  computed: {
    canGenerateChart() {
      return this.selectedXColumn && 
             this.selectedYColumns.length >= 1 && 
             this.selectedYColumns.length <= 2;
    }
  },
  
  watch: {
    data: {
      handler(newData) {
        if (newData && newData.success && newData.data) {
          this.processData();
        }
      },
      immediate: true
    }
  },
  
  
  methods: {
    
    processData() {
      this.isLoading = true;
      
      // 실제 데이터 처리 (최소 1초는 로딩 표시)
      const startTime = Date.now();
      const minLoadingTime = 1000;
      
      const processDataInternal = () => {
        const dataArray = this.data.data;
        if (dataArray && dataArray.length > 0) {
          const firstRow = dataArray[0];
          this.availableColumns = Object.keys(firstRow);
          this.numericColumns = this.getNumericColumns(dataArray);
          
          console.log('Available columns:', this.availableColumns);
          console.log('Numeric columns:', this.numericColumns);
          console.log('Sample data:', dataArray[0]);
        }
        this.isLoading = false;
      };
      
      const elapsedTime = Date.now() - startTime;
      const remainingTime = Math.max(0, minLoadingTime - elapsedTime);
      
      setTimeout(processDataInternal, remainingTime);
    },
    
    getNumericColumns(dataArray) {
      if (!dataArray || dataArray.length === 0) return [];
      
      const firstRow = dataArray[0];
      const numericCols = Object.keys(firstRow).filter(column => {
        const value = firstRow[column];
        
        // null이나 undefined는 제외
        if (value === null || value === undefined) return false;
        
        // 숫자 타입
        if (typeof value === 'number' && !isNaN(value)) return true;
        
        // 문자열이지만 숫자로 변환 가능한 경우
        if (typeof value === 'string') {
          const trimmed = value.trim();
          // 빈 문자열 제외
          if (trimmed === '') return false;
          // 숫자로 변환 가능한지 체크
          const num = Number(trimmed);
          return !isNaN(num) && isFinite(num);
        }
        
        return false;
      });
      
      console.log('Numeric column detection:', numericCols.map(col => ({
        column: col,
        value: firstRow[col],
        type: typeof firstRow[col]
      })));
      
      return numericCols;
    },
    
    selectXColumn(column) {
      // X축은 항상 하나만 선택 (라디오 버튼 동작)
      this.selectedXColumn = column;
    },
    
    selectYColumn(column) {
      const index = this.selectedYColumns.indexOf(column);
      
      if (index !== -1) {
        // 이미 선택된 경우 → 선택 해제
        this.selectedYColumns.splice(index, 1);
        // 알림이 표시 중이면 숨김
        if (this.showMaxYAlert) {
          this.showMaxYAlert = false;
          if (this.maxYAlertTimeout) {
            clearTimeout(this.maxYAlertTimeout);
            this.maxYAlertTimeout = null;
          }
        }
      } else {
        // 선택되지 않은 경우
        if (this.selectedYColumns.length < 2) {
          // 2개 미만이면 추가
          this.selectedYColumns.push(column);
        } else {
          // 이미 2개 선택된 상태 → 알림 표시
          this.showMaxYAlert = true;
          if (this.maxYAlertTimeout) {
            clearTimeout(this.maxYAlertTimeout);
          }
          this.maxYAlertTimeout = setTimeout(() => {
            this.showMaxYAlert = false;
            this.maxYAlertTimeout = null;
          }, 3000);
        }
      }
    },
    
    generateChart() {
      if (!this.canGenerateChart) {
        console.error('Cannot generate chart: requirements not met', {
          selectedXColumn: this.selectedXColumn,
          selectedYColumns: this.selectedYColumns,
          canGenerate: this.canGenerateChart
        });
        return;
      }
      
      console.log('Generating chart with:', {
        selectedXColumn: this.selectedXColumn,
        selectedYColumns: this.selectedYColumns
      });
      
      this.isChartGenerated = true;
      this.chartTitle = this.generateChartTitle();
      
      // DOM이 완전히 렌더링된 후 차트 생성
      this.$nextTick(() => {
        setTimeout(() => {
          this.createChart();
        }, 100);
      });
    },
    
    generateChartTitle() {
      const metadata = this.data.metadata;
      if (metadata && metadata.question) {
        // 질문에서 데이터셋 이름을 추출하여 간결하게 표시
        const question = metadata.question;
        
        // 패턴 매칭으로 데이터셋 이름 추출
        const patterns = [
          // "2024년 서울 화재 출동 데이터의 월별 발생 건수를 보여줘" -> "2024년 서울 화재 출동 데이터"
          /^(\d+년.*?데이터)(?:의|를|을).*$/,
          // "서울 화재 데이터를 보여줘" -> "서울 화재 데이터"
          /^(.*?데이터)(?:를|을|의).*$/,
          // "화재 현황을 보여줘" -> "화재 현황"
          /^(.*?현황)(?:을|를).*$/,
          // "화재 통계 분석해줘" -> "화재 통계"
          /^(.*?통계).*$/,
          // 기타 "XXX를/을/의" 패턴
          /^(.*?)(?:를|을|의|에서|별|당).*$/
        ];
        
        for (const pattern of patterns) {
          const match = question.match(pattern);
          if (match && match[1]) {
            return match[1].trim();
          }
        }
        
        // 패턴이 매칭되지 않으면 원본 질문 사용
        return question;
      }
      return `${this.selectedXColumn}별 ${this.selectedYColumns.join(', ')} 데이터`;
    },
    
    createChart() {
      const canvas = this.$refs.chartCanvas;
      if (!canvas) {
        console.error('Canvas element not found');
        return;
      }
      
      // 선택된 컬럼 유효성 검사 (더 관대하게 수정)
      if (!this.selectedXColumn) {
        console.error('No X column selected for chart creation');
        return;
      }
      if (this.selectedYColumns.length === 0) {
        console.error('No Y column selected for chart creation');
        return;
      }
      
      // Canvas 크기 강제 설정
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
      
      const ctx = canvas.getContext('2d');
      
      if (this.chartInstance) {
        this.chartInstance.destroy();
        this.chartInstance = null;
      }
      
      try {
        const chartData = this.prepareChartData();
        const chartOptions = this.getChartOptions();
        
        console.log('Creating chart with data:', chartData);
        console.log('Chart options:', chartOptions);
        
        this.chartInstance = new ChartJS(ctx, {
          type: 'line',
          data: chartData,
          options: chartOptions
        });
        console.log('Chart created successfully:', this.chartInstance);
      } catch (error) {
        console.error('Error creating chart:', error);
      }
    },
    
    updateChart() {
      if (!this.canGenerateChart) {
        console.warn('Cannot generate chart - requirements not met');
        return;
      }
      
      // 차트 제목 업데이트
      this.chartTitle = this.generateChartTitle();
      
      // 차트 재생성 전에 기존 차트 확실히 정리
      if (this.chartInstance) {
        this.chartInstance.destroy();
        this.chartInstance = null;
      }
      
      // 차트 재생성
      this.$nextTick(() => {
        setTimeout(() => {
          this.createChart();
        }, 100); // 시간을 조금 더 늘려서 DOM 업데이트 보장
      });
    },
    
    prepareChartData() {
      const dataArray = this.data.data;
      if (!dataArray || dataArray.length === 0) {
        console.error('No data available for chart');
        return { labels: [], datasets: [] };
      }
      
      const labels = dataArray.map(row => row[this.selectedXColumn]);
      
      const datasets = this.selectedYColumns.map((column, index) => {
        const data = dataArray.map(row => {
          const value = row[column];
          return typeof value === 'number' ? value : Number(value) || 0;
        });
        
        const colors = ['#22C55E', '#A855F7', '#3B82F6', '#F59E0B'];  // 초록, 보라, 파랑, 노랑
        const color = colors[index % colors.length];
        
        return {
          label: column,
          data: data,
          borderColor: color,
          backgroundColor: color + '20',
          borderWidth: 3,
          pointRadius: 6,
          pointHoverRadius: 8,
          pointBorderWidth: 0,
          pointBackgroundColor: color,
          tension: 0.2,
          yAxisID: this.selectedYColumns.length === 2 ? (index === 0 ? 'y' : 'y1') : 'y',
          visible: true
        };
      });
      
      this.chartDatasets = datasets;
      
      return {
        labels,
        datasets
      };
    },
    
    getChartOptions() {
      const isDualYAxis = this.selectedYColumns.length === 2;
      
      const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false  // 커스텀 범례 사용
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#fff',
            bodyColor: '#fff',
            borderColor: '#ccc',
            borderWidth: 1
          }
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: this.selectedXColumn,
              font: {
                size: 14,
                weight: 'bold'
              }
            },
            grid: {
              display: false
            }
          },
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            title: {
              display: true,
              text: this.selectedYColumns[0],
              font: {
                size: 14,
                weight: 'bold'
              }
            },
            grid: {
              display: false
            }
          }
        },
        interaction: {
          intersect: false,
          mode: 'index'
        }
      };
      
      // 듀얼 Y축 설정
      if (isDualYAxis) {
        options.scales.y1 = {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: this.selectedYColumns[1],
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          grid: {
            display: false
          }
        };
      }
      
      return options;
    },
    
    toggleDataset(index) {
      if (!this.chartInstance) return;
      
      const meta = this.chartInstance.getDatasetMeta(index);
      
      meta.hidden = !meta.hidden;
      this.chartDatasets[index].visible = !meta.hidden;
      
      this.chartInstance.update();
    }
  },
  
  beforeUnmount() {
    if (this.chartInstance) {
      this.chartInstance.destroy();
    }
    if (this.maxYAlertTimeout) {
      clearTimeout(this.maxYAlertTimeout);
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 1000px;
  height: 900px;
  min-width: 600px;
  min-height: 600px;
  max-width: 95vw;
  max-height: 95vh;
  background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  position: relative;
  padding: 50px 60px;
  display: flex;
  flex-direction: column;
}

/* 로딩 스타일 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
}

.loading-text {
  margin-top: 20px;
  font-size: 18px;
  color: #2744FF;
  font-weight: 500;
}

/* 정보 버튼 */
.info-button {
  position: absolute;
  top: 24px;
  right: 24px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid #D1D5DB;
  background: #F9FAFB;
  color: #6B7280;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.info-button:hover {
  border-color: #2744FF;
  background: #2744FF;
  color: white;
}

/* 툴팁 */
.tooltip {
  position: absolute;
  top: 60px;
  right: 24px;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  max-width: 300px;
  font-size: 14px;
  line-height: 1.4;
  color: #374151;
  z-index: 1001;
  text-align: left;
  font-weight: 400;
}

.tooltip::before {
  content: '';
  position: absolute;
  top: -8px;
  right: 20px;
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid white;
}

/* 컬럼 선택 화면 */
.column-selection {
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: center;
  align-items: center;
  position: relative;
}

.selection-title {
  font-size: 36px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 60px 0;
  text-align: center;
  position: relative;
}

.selection-title::after {
  content: '';
  position: absolute;
  bottom: -15px;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 4px;
  background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.axis-selection-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
  width: 100%;
  max-width: 700px;
  margin-bottom: 60px;
}

.axis-section {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.axis-section:hover {
  transform: translateY(-4px);
  box-shadow: 
    0 16px 50px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.axis-title {
  font-size: 22px;
  font-weight: 700;
  background: linear-gradient(135deg, #2744FF 0%, #4338CA 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 24px;
  position: relative;
  display: inline-block;
  text-align: center;
  width: 100%;
}

.axis-title::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #2744FF, transparent);
  border-radius: 2px;
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  justify-items: center;
}

.checkbox-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 14px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  user-select: none;
  position: relative;
  overflow: hidden;
  white-space: nowrap;
  min-width: 160px;
}

.checkbox-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(103, 126, 234, 0.15), transparent);
  transition: left 0.6s ease;
}

.checkbox-item:hover::before {
  left: 100%;
}

.checkbox-item:hover {
  transform: translateY(-3px);
  border-color: rgba(103, 126, 234, 0.4);
  box-shadow: 0 12px 30px rgba(103, 126, 234, 0.2);
  background: rgba(255, 255, 255, 0.95);
}

.checkbox-item.selected {
  background: linear-gradient(135deg, rgba(103, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
  border-color: #667eea;
  box-shadow: 
    0 8px 25px rgba(103, 126, 234, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.checkbox-item.selected .checkbox-label {
  color: #667eea;
  font-weight: 600;
}

.checkbox-item input[type="checkbox"] {
  margin-right: 12px;
  width: 20px;
  height: 20px;
  accent-color: #667eea;
  border-radius: 6px;
}

.checkbox-label {
  font-size: 15px;
  font-weight: 500;
  color: #374151;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}

.select-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 18px;
  padding: 18px 48px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 
    0 12px 35px rgba(103, 126, 234, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  overflow: hidden;
  position: relative;
  align-self: center;
}

.select-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.6s ease;
}

.select-button:hover::before {
  left: 100%;
}

.select-button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 
    0 15px 40px rgba(103, 126, 234, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.select-button:active:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 
    0 5px 15px rgba(103, 126, 234, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.select-button:disabled {
  background: linear-gradient(145deg, #E5E7EB 0%, #D1D5DB 100%);
  cursor: not-allowed;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
  color: #9CA3AF;
}

/* 최대 선택 알림 */
.max-y-alert {
  position: fixed;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  background: #FEF3C7;
  border: 1px solid #F59E0B;
  color: #92400E;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
  z-index: 1002;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* 차트 결과 화면 */
.chart-result {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding-bottom: 5px;
}

.chart-title {
  font-size: 24px;
  font-weight: 600;
  color: #2744FF;
  text-align: center;
  margin-bottom: 48px;
}

/* 범례 및 컬럼 재선택 통합 영역 */
.legend-and-reselection {
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  padding: 12px 16px 16px 16px;
  margin-bottom: 16px;
  overflow: visible;
}

.legend-section {
  margin-bottom: 12px;
}

.legend-controls {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  gap: 20px;
  padding: 0;
  margin-left: 0;
}

.legend-item {
  display: flex;
  align-items: center;
  padding: 4px 0;
  border-radius: 4px;
  margin-right: 16px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  margin-right: 6px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.legend-label {
  font-size: 12px;
  font-weight: 500;
  color: #374151;
}

/* 컬럼 재선택 영역 */
.column-reselection {
  padding: 0;
  margin: 0;
}

.reselection-section {
  margin-bottom: 12px;
}

.reselection-section:last-child {
  margin-bottom: 0;
}

.reselection-title {
  font-size: 12px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 4px;
}

.reselection-checkboxes {
  display: block;
  text-align: left;
}

.reselection-checkbox-item {
  display: inline-block;
  align-items: center;
  padding: 3px 8px 3px 0;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
  vertical-align: top;
}

.reselection-checkbox-item:hover .reselection-checkbox-label {
  color: #2744FF;
}

.reselection-checkbox-item input[type="checkbox"] {
  margin-right: 4px;
  width: 14px;
  height: 14px;
  accent-color: #2744FF;
  vertical-align: middle;
}

.reselection-checkbox-label {
  font-size: 11px;
  font-weight: 500;
  color: #374151;
  transition: color 0.2s;
  vertical-align: middle;
}

.chart-container {
  height: 500px;
  position: relative;
  margin-bottom: 16px;
}

/* 구분선 */
.divider {
  height: 1px;
  background: #E5E7EB;
  margin: 16px 0;
}
</style>