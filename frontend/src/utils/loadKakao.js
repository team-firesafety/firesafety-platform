/** 카카오 SDK를 동적으로 로드하고, 로드 완료 후 window.kakao 객체를 반환 */
export function loadKakao() {
    return new Promise((resolve) => {
        /* 이미 로드돼 있으면 바로 resolve */
        if (window.kakao && window.kakao.maps) return resolve(window.kakao);

        /* 스크립트 태그 삽입 */
        const script = document.createElement('script');
        script.src =
            `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${import.meta.env.VITE_KAKAO_MAP_KEY}`;
        script.onload = () => {
            window.kakao.maps.load(() => resolve(window.kakao));
        };
        document.head.appendChild(script);
    });
}
