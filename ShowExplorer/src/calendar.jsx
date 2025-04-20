import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export const Calendar = ({ showDays, days = 14 }) => {
  return (
    <div id="calendar-full">
      <div id="days" className="mobile-hidden">
        <h4>Sun</h4>
        <h4>Mon</h4>
        <h4>Tue</h4>
        <h4>Wed</h4>
        <h4>Thu</h4>
        <h4>Fri</h4>
        <h4>Sat</h4>
      </div>
      <div id="calendar">
        {showDays &&
          Object.keys(showDays).map((day) => (
            <CalendarDay
              key={day}
              day={day}
              showList={showDays[day]}
            ></CalendarDay>
          ))}
      </div>
    </div>
  );
};

const CalendarDay = ({ day, showList }) => {
  return (
    <div className={`calendar-day`} key={day}>
      <div>
        <h4 className="calendar-date">{day}</h4>
        <div className="calendar-day-band-list">
          {showList.map((show, y) => (
            <p
              className={y > 11 ? "overflow-show" : ""}
              key={show["artist_name"]}
            >
              {show["artist_name"]}
            </p>
          ))}
          {Object.entries(showList).map(([key, venue]) => {
            return (
              <div key={key}>
                {venue.map((show, y) => {
                  return (
                    <p
                      className={y > 11 ? "overflow-show" : ""}
                      key={show["artist_name"]}
                    >
                      {show["artist_name"]}
                    </p>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>
      {Object.keys(showList)[0] && (
        <Link to={`Boise/${day}`} className="expanded-day-link">
          Show More
        </Link>
      )}
    </div>
  );
};
