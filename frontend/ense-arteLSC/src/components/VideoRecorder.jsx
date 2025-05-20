import { useState, useRef } from "react";
import { Bouncy } from "ldrs/react";
import "ldrs/react/Bouncy.css";

const VideoRecorder = ({ recording, setRecording }) => {
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);

  const [videoURL, setVideoURL] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const startRecording = async () => {
    try {
      setVideoURL(null); // reset video para nueva grabación

      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      const chunks = [];
      mediaRecorder.ondataavailable = (event) => chunks.push(event.data);
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: "video/webm" });
        const url = URL.createObjectURL(blob);
        setVideoURL(url);

        videoRef.current.srcObject = null;
        videoRef.current.src = url;

        // Activar modo "procesando"
        setIsProcessing(true);
        setTimeout(() => {
          setIsProcessing(false);
        }, 5000); // Simula procesamiento por 3 segundos
      };

      mediaRecorder.start();
      setRecording(true);
    } catch (error) {
      console.error("Error al acceder a la cámara:", error);
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    videoRef.current.srcObject?.getTracks().forEach((track) => track.stop());
    setRecording(false);
  };

  return (
    <div className="flex flex-row">
      {/* Sección izquierda: video y botones (idéntico al original) */}
      <div className="flex flex-col items-center relative">
        <video
          ref={videoRef}
          autoPlay
          muted
          loop
          controls={false}
          style={{ width: "399px", height: "296px", backgroundColor: "black" }}
          className="border"
        />
        {!videoURL && (
          <button
            className="absolute bottom-2 cursor-pointer"
            onClick={recording ? stopRecording : startRecording}
          >
            <img
              src={recording ? "./assets/stop.png" : "./assets/rec.png"}
              className={recording ? "h-10 w-10 mx-auto" : "h-8 w-8 mx-auto"}
              alt=""
            />
          </button>
        )}
      </div>

      {/* Sección derecha: texto o loader */}
      <div className="w-[399px] h-[296px] bg-[#2241A0] flex items-center justify-center">
        {isProcessing ? (
          // Spinner centrado mientras se procesa
          <Bouncy size="45" speed="1.75" color="white" />
        ) : (
          <div className="flex flex-col items-center justify-center gap-4 p-4">
            <img
              className="w-[40px] h-[40px]"
              src="./assets/camara.png"
              alt=""
            />
            <h1 className="text-white font-bold text-lg text-center">
              {recording
                ? "Para pausar la grabación selecciona el botón rojo de la izquierda."
                : "Al hacer clic en el botón verde, aceptas ser grabado. No se guardará tu video."}
            </h1>
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoRecorder;
