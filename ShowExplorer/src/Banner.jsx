import { useContext, useEffect, useState } from "react";

import {
  generateVerifierAndChallengAndGetAuthCode,
  retrieveAndStoreToken,
  saveProfileAsUser,
} from "./Users/authHelpers";
import { ProfileContext } from "./ProfileContext";

export const getProfile = async () => {
  let accessToken = localStorage.getItem("access_token");
  const response = await fetch("https://api.spotify.com/v1/me", {
    headers: {
      Authorization: "Bearer " + accessToken,
    },
  });

  const data = await response.json();

  const createdUser = saveProfileAsUser(data)
    .then((res) => {
      console.log(`create user : ${res}`);
    })
    .then((prof) => {
      return prof;
    });

  return data;
};

export const Banner = ({ setProfile }) => {
  let profile = useContext(ProfileContext);
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    let code = urlParams.get("code");
    if (code && !localStorage.getItem("access_token")) {
      retrieveAndStoreToken(code).then(() => {
        getProfile().then((data) => {
          setProfile(data);
        });
      });
    }
    if (!profile && localStorage.getItem("access_token")) {
      getProfile().then((data) => {
        setProfile(data);
      });
    }
  }, []);

  return (
    <div id="banner">
      <h1>Local Shows</h1>
      <div id="user-group">
        {profile && profile.images && profile.images[0] && (
          <img id="profile-img" src={profile.images[0].url} />
        )}
        {!localStorage.getItem("access_token") && (
          <button onClick={generateVerifierAndChallengAndGetAuthCode}>
            Login
          </button>
        )}
        {localStorage.getItem("access_token") && (
          <button
            onClick={() => {
              localStorage.removeItem("access_token");
              localStorage.removeItem("code_verifier");
              window.location.search = "";
            }}
          >
            Logout
          </button>
        )}
      </div>
    </div>
  );
};

export default Banner;
