import { useLoaderData } from "react-router";
import { Calendar } from "./calendar";
import { useContext, useEffect, useState } from "react";
import { ArtistsContext } from "./ArtistContext";
import { Playlist } from "./playlist";

export const Home = (getData, setData, profile, artistsAndShows) => {
  let showDays = useLoaderData();
  let artistData = useContext(ArtistsContext);

  console.log(artistData);

  return (
    <div className="main-content">
      <Calendar showDays={showDays} />
      <Playlist />
    </div>
  );
};

export const SpotifyWrapper = (
  getData,
  setData,
  profile,
  artistsAndShows,
  child
) => {
  useEffect(() => {
    console.log("Starting data check");
    console.log(profile);

    if (profile) {
      console.log("has profile");
      artistData = getData();
      setData(artistData);
      console.log(artistData);
    }
  }, []);

  return { child };
};
