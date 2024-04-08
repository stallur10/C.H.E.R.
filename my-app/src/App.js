import React, { useState } from "react";
import "./App.css";
import { db } from "./firebase-config";
import { doc, setDoc } from "firebase/firestore";

function App() {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [percent, setPercent] = useState("");
  const [message, setMessage] = useState("");
  const [timeLim, setTimeLim] = useState("");


  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const userRef = doc(db, "Users", "User1");
      await setDoc(userRef, {
        Message: message,
        PhoneNumber: phoneNumber,
        Percent: percent,
        TimeLimit: timeLim,
      });
      console.log("Document successfully written!");

      setPhoneNumber("");
      setPercent("");
      setMessage("");
      setTimeLim("")
    } catch (e) {
      console.error("Error adding document: ", e);
    }
  };

  return (
    <div className="App">
      <div className="App-content">
        <header className="App-header">
          <h1>CONFIGURE C.H.E.R. </h1>
        </header>
        <form onSubmit={handleSubmit}>
          <div className="Questions">
            <div>
              <label>
                Phone Number
                <input
                  type="text"
                  placeholder="Enter"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                />
              </label>
            </div>
            <div>
              <label>
                Trigger Message at What Percent?
                <input
                  type="text"
                  placeholder="Enter"
                  value={percent}
                  onChange={(e) => setPercent(e.target.value)}
                />
              </label>
            </div>
            <div>
              <label>
                Message
                <input
                  type="text"
                  placeholder="Enter"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                />
              </label>
            </div>
            <div>
              <label>
                Session Length (Seconds)
                <input
                  type="text"
                  placeholder="Enter"
                  value={timeLim}
                  onChange={(e) => setTimeLim(e.target.value)}
                />
              </label>
            </div>
            <button type="submit">Submit</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
