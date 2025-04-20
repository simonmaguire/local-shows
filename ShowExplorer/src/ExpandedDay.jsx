import { Link, useParams, useLoaderData } from "react-router-dom";
import { useContext } from "react";
import { ArtistsContext } from "./ArtistContext";
import { ProfileContext } from "./ProfileContext";
import { UserShowsContext } from "./UserShowsContext";

const saveShow = async (user_id, show_id) => {
  const response = await fetch("http://127.0.0.1:5000/api/saveShow", {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({ user: user_id, show: show_id }),
  });
};

const removeShow = async (user_id, show_id) => {
  const response = await fetch("http://127.0.0.1:5000/api/removeShow", {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({ user: user_id, show: show_id }),
  });
};

const ShowActionButton = ({ concert_id, profile }) => {
  let { userShows, setUserShows } = useContext(UserShowsContext);
  if (!userShows) {
    return <></>;
  }
  let showSaved = userShows.includes(concert_id);
  let newUserShows = [...userShows];
  newUserShows = !showSaved
    ? [...newUserShows, concert_id]
    : newUserShows.filter((concert) => concert !== concert_id);
  console.log(newUserShows);
  return showSaved ? (
    <button
      onClick={() =>
        removeShow(profile.id, concert_id).then(() => {
          setUserShows([...newUserShows]);
        })
      }
    >
      Remove
    </button>
  ) : (
    <button
      onClick={() =>
        saveShow(profile.id, concert_id).then(() => {
          setUserShows([...newUserShows]);
        })
      }
    >
      Add
    </button>
  );
};

export const ExpandedDay = () => {
  let showDays = useLoaderData();
  let { showDate } = useParams();
  let showList = showDays[showDate];

  let showsWithSpotify = useContext(ArtistsContext);
  let profile = useContext(ProfileContext);

  showList = showsWithSpotify ? showsWithSpotify[showDate] : showList;

  console.log(showList);
  return (
    <div className="expanded-day">
      <h2>{showDate}</h2>
      <div id="shows-info">
        <div id="show-info-header">
          <h3>Band</h3>
          <h3>Venue</h3>
          {/* <h3>Actions</h3> */}
        </div>
        {Object.entries(showList).map(([key, venue]) => {
          console.log("VENUE: ");
          console.log(venue);
          return (
            <div className="concert-group" key={key}>
              <div className="concert-artists">
                {venue.map((show, y) => {
                  return <p key={show["artist_name"]}>{show["artist_name"]}</p>;
                })}
              </div>
              <p>{key}</p>
              {venue[0]["venue_same_as"] ? (
                <a target="_blank" href={venue[0]["venue_same_as"]}>
                  visit website{" "}
                </a>
              ) : null}
              <ShowActionButton
                concert_id={venue[0]["concert_id"]}
                profile={profile}
              />
            </div>
          );
        })}
      </div>
      <Link to={`/`}>Return</Link>
    </div>
  );
};

// {showList.map((show, y) => (
//   <div className="show-row" key={show["artist_name"]}>
//     <p>{show["artist_name"]}</p>
//     {show["artist_info"] && show["artist_info"]["genres"] ? (
//       <p>{show["artist_info"]["genres"][0] ?? ""} </p>
//     ) : (
//       <p></p>
//     )}
//     <p>{show["venue"]}</p>
//     {/* <p>{show["venue_same_as"] ? "visit website" : null}</p> */}
//     {show["venue_same_as"] ? (
//       <a target="_blank" href={show["venue_same_as"]}>
//         visit website{" "}
//       </a>
//     ) : null}
//     <button onClick={() => saveShow(profile.id, show["concert_id"])}>
//       Add
//     </button>
//   </div>
// ))}
