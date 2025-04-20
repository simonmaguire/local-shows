import { useState, useEffect, useContext } from "react";
import "./App.css";
import { Home, SpotifyWrapper } from "./Home";
import { ExpandedDay } from "./ExpandedDay";
import { Banner } from "./Banner";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ArtistsContext } from "./ArtistContext";
import { ProfileContext } from "./ProfileContext";
import { UserShowsContext } from "./UserShowsContext";

const saveSpotifyID = async (concert_id, artist_id, artist_spotify_id) => {
  const response = await fetch("http://127.0.0.1:5000/api/saveSpotifyID", {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({
      concert_id: concert_id,
      artist_id: artist_id,
      artist_spotify_id: artist_spotify_id,
    }),
  });
};

const formatShowData = (numberDays, shows) => {
  var calendarShowData = {};
  var currentDate = new Date();
  var endDate = new Date();
  endDate = endDate.setDate(currentDate.getDate() + numberDays);

  var tempDate = new Date();

  //TODO: Kind of hacky for now, but back filling days array so calendar formats easily starting with sunday
  while (currentDate.getDay() != 0 || currentDate.getDay() != "0") {
    currentDate.setDate(currentDate.getDate() - 1);
  }

  while (currentDate <= endDate) {
    calendarShowData[`${currentDate.getMonth() + 1}-${currentDate.getDate()}`] =
      [];
    currentDate.setDate(currentDate.getDate() + 1);
  }
  // debugger;
  Array.isArray(shows) &&
    shows.forEach((show) => {
      // debugger;
      let dateDeconstructed = show["show_date"].split("-");
      let venue = show["venue"];
      let day = parseInt(dateDeconstructed[2]);
      let showDate = `${parseInt(dateDeconstructed[1])}-${day}`;
      calendarShowData[showDate]
        ? calendarShowData[showDate][show["venue"]]
          ? calendarShowData[showDate][show["venue"]].push(show)
          : (calendarShowData[showDate][show["venue"]] = [show])
        : null;
      // calendarShowData[showDate]
      //   ? calendarShowData[showDate][show["venue"]].push(show)
      //   : null;
    });

  console.log(calendarShowData);

  return calendarShowData;
};

const formatShowandArtistData = (numberDays, shows, artists) => {
  var calendarShowData = {};
  var currentDate = new Date();
  var endDate = new Date();
  endDate = endDate.setDate(currentDate.getDate() + numberDays);

  var tempDate = new Date();

  //TODO: Kind of hacky for now, but back filling days array so calendar formats easily starting with sunday
  while (currentDate.getDay() != 0 || currentDate.getDay() != "0") {
    currentDate.setDate(currentDate.getDate() - 1);
  }

  while (currentDate <= endDate) {
    calendarShowData[`${currentDate.getMonth() + 1}-${currentDate.getDate()}`] =
      [];
    currentDate.setDate(currentDate.getDate() + 1);
  }
  // debugger;
  let artistsCounter = 0;
  Array.isArray(shows) &&
    shows.forEach((show) => {
      // debugger;
      show.artist_info = artists[artistsCounter];
      saveSpotifyID(
        show["concert_id"],
        show["artist_id"],
        show["artist_info"]["id"]
      );
      let dateDeconstructed = show["show_date"].split("-");
      let day = parseInt(dateDeconstructed[2]);
      let showDate = `${parseInt(dateDeconstructed[1])}-${day}`;
      // calendarShowData[showDate] ? calendarShowData[showDate].push(show) : null;
      calendarShowData[showDate]
        ? calendarShowData[showDate][show["venue"]]
          ? calendarShowData[showDate][show["venue"]].push(show)
          : (calendarShowData[showDate][show["venue"]] = [show])
        : null;
      artistsCounter = artistsCounter + 1;
    });

  return calendarShowData;
};

const getShowData = async () => {
  let showData = await fetch("http://127.0.0.1:5000/api/getShows")
    .then((res) => res.json())
    .then((data) => {
      return formatShowData(13, data);
    })
    .then((showData) => showData);
  return showData;
};

const getShowAndArtistData = async () => {
  let data = await fetch("http://127.0.0.1:5000/api/getArtistsFromShows", {
    method: "get",
    headers: new Headers({
      Authorization: `Bearer ${localStorage.getItem("access_token")}`,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      return formatShowandArtistData(13, data["shows"], data["artists"]);
    })
    .then((showsAndArtists) => {
      return showsAndArtists;
    });
  return data;
};

const getUserShows = async (user_id) => {
  let data = await fetch(`http://127.0.0.1:5000/api/getUserShows/${user_id}`, {
    method: "get",
    headers: new Headers({
      Authorization: `Bearer ${localStorage.getItem("access_token")}`,
    }),
  }).then((res) => res.json());
  return data;
};

const getArtistsSpotifyIds = async (listUserShows) => {
  let listArtistsSpotifyIDs = [];
  await Promise.all(
    listUserShows.map(async (concert_id) => {
      let data = await fetch(
        `http://127.0.0.1:5000/api/spotifyArtistAtConcert/${concert_id}`,
        {
          method: "get",
        }
      );
      let res = await data.json();

      res.map((id) => {
        if (id) {
          listArtistsSpotifyIDs.push(id);
        }
      });
    })
  );
  return listArtistsSpotifyIDs;
};

const getTopTracks = async (listUserShows) => {
  let listArtistsSpotifyIDs = await getArtistsSpotifyIds(listUserShows);

  let userShowsTopTracks = [];
  console.log("SPOTIFY IDS \n", listArtistsSpotifyIDs);
  await Promise.all(
    listArtistsSpotifyIDs.map(async (artist_spotify_id) => {
      let res = await fetch(
        `http://127.0.0.1:5000/api/getTopTracks/${artist_spotify_id}`,
        {
          method: "get",
          headers: new Headers({
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          }),
        }
      );
      let topTracks = await res.json();

      topTracks.map((track) => {
        userShowsTopTracks.push(track);
      });
    })
  );
  return userShowsTopTracks;
};

const router = createBrowserRouter([
  {
    path: "/",
    loader: getShowData,
    element: <Home />,
  },
  {
    path: "/:city/:showDate",
    loader: getShowData,
    element: <ExpandedDay />,
  },
]);

function App() {
  const [profile, setProfile] = useState(undefined);
  const [spotifyData, setSpotifyData] = useState(undefined);
  const [userShows, setUserShows] = useState([]);
  const [topTracks, setTopTracks] = useState([]);

  useEffect(() => {
    if (profile) {
      getShowAndArtistData().then((data) => {
        setSpotifyData(data);
      });
      getUserShows(profile.id)
        .then((data) => {
          setUserShows(data);
          console.log(data);
          return data;
        })
        .then((data) => {
          getTopTracks(data).then((trackRes) => {
            setTopTracks(trackRes);
          });
        });
    }
  }, [profile]);

  const changeProfile = (newProfile) => {
    setProfile(newProfile);
  };

  return (
    <>
      <ProfileContext.Provider value={profile}>
        <Banner setProfile={changeProfile}></Banner>
        <UserShowsContext.Provider
          value={{ userShows, setUserShows, topTracks }}
        >
          <ArtistsContext.Provider value={spotifyData}>
            <RouterProvider router={router} />
          </ArtistsContext.Provider>
        </UserShowsContext.Provider>
      </ProfileContext.Provider>
    </>
  );
}

export default App;
