
export async function fetchWithAuth(url, options = {}) {
  const accessToken = localStorage.getItem("access_token");

  // 최종 구현 완료시에 5~18줄은 지워야함 현재 페이지를 못건너 뛰어 하드코딩으로 박아놓았음
  if (
    process.env.NODE_ENV === "development" &&
    url.endsWith("/user/me")
  ) {
    console.warn(" [DEV MODE] /user/me 응답을 mock으로 대체합니다");
    return {
      status: 200,
      json: async () => ({
        username: "dev_user",
        email: "dev@example.com",
      }),
    };
  }
//----------------------------------------------- 이 위에를 지워야함 -----------


  // 최초 요청
  let response = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });

  // access_token 만료된 경우 처리
  if (response.status === 401) {
    const errorData = await response.json();
    if (errorData.detail === "Expired token") {
      console.warn("Access token expired. Attempting to refresh...");

      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        alert("No refresh token available. Please log in again.");
        localStorage.clear();
        window.location.href = "/login";
        return;
      }

      const refreshResponse = await fetch("http://localhost:8000/auth/token/refresh", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (refreshResponse.status === 200) {
        const newToken = await refreshResponse.json();
        localStorage.setItem("access_token", newToken.access_token);

        // 원래 요청 재시도
        return fetch(url, {
          ...options,
          headers: {
            ...(options.headers || {}),
            Authorization: `Bearer ${newToken.access_token}`,
            "Content-Type": "application/json",
          },
        });
      } 
      
      const refreshError = await refreshResponse.json();

      if (refreshResponse.status === 400 && refreshError.detail === "Missing refresh token") {
        alert("Missing refresh token. Please log in again.");
      } 

      else if (refreshResponse.status === 401 && refreshError.detail === "Invalid token") {
        alert("Invalid refresh token. Please log in again.");
      }
      
      else if (refreshResponse.status === 401 && refreshError.detail === "Expired token") {
        alert("Refresh token has expired. Please log in again.");
      }
      
      else if (refreshResponse.status === 403 && refreshError.detail === "Revoked token") {
        alert("Refresh token has been revoked. Please log in again.");
      } 
      
      else if (refreshResponse.status === 500) {
        alert("Unexpected server error during token refresh.");
      } 
      
      else {
        alert("Unknown error during token refresh: " + refreshError.detail);
      }

      // 모든 실패 시 로그아웃 처리
      localStorage.clear();
      window.location.href = "/login";
      return;
    }
  }

  return response;
}
