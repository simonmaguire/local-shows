import { useContext } from "react";
import { ArtistsContext } from "./ArtistContext";
import { UserShowsContext } from "./UserShowsContext";
import { ProfileContext } from "./ProfileContext";

const getTopTracks = async (artist_id) => {
  let topTracks = await fetch(
    `https://api.spotify.com/v1/artists/${artist_id}/top-tracks`,
    {
      method: "get",
      headers: new Headers({
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      }),
    }
  ).then((res) => res.json());
  return topTracks;
};

const createPlaylist = async (user_id, topTracks) => {
  let result = await fetch(`http://127.0.0.1:5000/api/createPlaylist`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ user_id: user_id, songs: topTracks }),
  });
};

export const Playlist = () => {
  let { userShows, setUserShows, topTracks } = useContext(UserShowsContext);
  let artistData = useContext(ArtistsContext);
  let profile = useContext(ProfileContext);
  return (
    <div>
      <div id="playlist-header">
        <h3>Your Show Playlist</h3>
        <button
          onClick={() => {
            let songURIs = [];
            topTracks.map((track) => {
              songURIs.push(track.uri);
            });
            createPlaylist(profile.id, songURIs);
          }}
        >
          <p>Create Playlist</p>
        </button>
      </div>
      <div id="playlist-song-container">
        {topTracks.map((track, y) => (
          <PlaylistSong key={y} track={track} />
        ))}
      </div>
    </div>
  );
};

const PlaylistSong = ({ track }) => {
  console.log(track);
  return (
    <div className="playlist-song">
      <img src={track.image} className="img-placeholder" />
      {/* <div className="img-placeholder"></div> */}
      <div className="playlist-song-details">
        <p>{track.name}</p>
        <p>{track.artist}</p>
        <p>{track.album}</p>
      </div>
    </div>
  );
};
