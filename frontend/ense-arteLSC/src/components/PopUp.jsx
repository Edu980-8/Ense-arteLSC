import VideoRecorder from "./VideoRecorder";
import { useState } from "react";
const PopUp = ({ setPopUp }) => {
  const [recording, setRecording] = useState(false);
  return (
    <div className="fixed top-0 left-0 w-full h-full bg-[#2241A0]/10 flex items-center justify-center z-50">
      <div className="flex flex-row  items-center bg-white  shadow-lg  w-1/3 ">
        <VideoRecorder recording={recording} setRecording={setRecording} />
        <img
          className=" w-[20px] h-[20px] absolute justify-end right-10 top-5 z-40"
          onClick={() => setPopUp(false)}
          src="./assets/close.svg"
          alt=""
        />
      </div>
    </div>
  );
};

export default PopUp;
