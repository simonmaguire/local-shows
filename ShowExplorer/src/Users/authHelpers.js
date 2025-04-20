export const generateRandomString = (length) => {
  let text = "";
  let possible =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (let i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
};

export async function generateCodeChallenge(codeVerifier) {
  function base64encode(string) {
    return btoa(String.fromCharCode(...new Uint8Array(string)))
      .replace(/\+/g, "-")
      .replace(/\//g, "_")
      .replace(/=+$/, "");
  }

  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await window.crypto.subtle.digest("SHA-256", data);

  return base64encode(digest);
}

export const generateVerifierAndChallengAndGetAuthCode = () => {
  const codeVerifier = generateRandomString(96);

  generateCodeChallenge(codeVerifier).then((codeChallenge) => {
    let state = generateRandomString(16);
    let scope =
      "user-read-private user-library-read user-read-email playlist-modify-public";

    localStorage.setItem("code_verifier", codeVerifier);

    let client_id = import.meta.env.VITE_SPOTIFY_CLIENT_ID;

    let args = new URLSearchParams({
      response_type: "code",
      client_id: client_id,
      scope: scope,
      redirect_uri: "http://localhost:5173/",
      state: state,
      code_challenge_method: "S256",
      code_challenge: codeChallenge,
    });

    window.location.href = "https://accounts.spotify.com/authorize?" + args;
  });
};

export const retrieveAndStoreToken = async (code) => {
  let codeVerifier = localStorage.getItem("code_verifier") || "";

  let client_id = import.meta.env.VITE_SPOTIFY_CLIENT_ID;

  let body = new URLSearchParams({
    grant_type: "authorization_code",
    code: code,
    redirect_uri: "http://localhost:5173/",
    client_id: client_id,
    code_verifier: codeVerifier,
  });

  const response = await fetch("https://accounts.spotify.com/api/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: body,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("HTTP status " + response.status);
      }
      return response.json();
    })
    .then((data) => {
      localStorage.setItem("access_token", data.access_token);
      console.log(data.access_token);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

export const saveProfileAsUser = async (profile) => {
  if ("id" in profile == false) {
    return "No User ID";
  }
  const userProfile = {
    spotify_id: profile.id,
    username: profile.display_name ?? "",
    email: profile.email ?? "",
    product: profile.product ?? "",
    country: profile.country ?? "",
  };

  const response = await fetch("http://127.0.0.1:5000/api/saveProfileAsUser", {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({ profile: userProfile }),
  });

  return response.json();
};
