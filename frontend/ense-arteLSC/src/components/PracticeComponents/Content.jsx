import { useState, useEffect } from "react";
import VideoRecorder from "../VideoRecorder";
import { Listbox } from "@headlessui/react";

const Content = () => {
  const [allSigns, setAllSigns] = useState([]);
  const [selected, setSelected] = useState(null);
  const [recording, setRecording] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/signs");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const responseBody = await response.json();
        console.log("Signs Data from Backend:", responseBody);

        if (responseBody && responseBody.data) {
          const signsData = responseBody.data;
          setAllSigns(signsData);
          setSelected(signsData[0] || null); // Valor por defecto: primera seña
        } else {
          setAllSigns([]);
          setSelected(null);
        }
      } catch (error) {
        console.log("Error al obtener datos:", error);
        setAllSigns([]);
        setSelected(null);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="z-10 h-screen w-[80%] overflow-y-auto">
      <section className="flex flex-col items-center justify-center">
        <section className="flex flex-row items-center gap-[80px]">
          <img
            className="mt-[5rem] ml-[9.125rem] max-w-[10.563rem] max-h-[13.625rem]"
            src="./assets/robot_evaluador.svg"
            alt="Robot evaluador"
          />
          <div className="flex flex-col gap-[1.5rem]">
            <h1 className="mt-[5rem] text-[24px] max-w-[32.563rem]">
              PON A PRUEBA TU CONOCIMIENTO{" "}
              <span className="font-bold">LA IA TE ACOMPAÑA</span>
            </h1>
            <ul className="text-[16px] max-w-[33.938rem]">
              <li className="text-md">
                <span className="font-bold">1. Te calificaremos:</span> Es
                momento de poner en práctica todo lo aprendido en el módulo de
                aprendizaje.
              </li>
              <li className="text-md">
                <span className="font-bold">2. Nuestro sistema te ayudará:</span>{" "}
                Aquí podrás grabarte o usar tu cámara para realizar las señas y
                nuestra IA evaluará si lo estás haciendo correctamente.
              </li>
              <li className="text-md">
                <span className="font-bold">3. Inténtalo varias veces:</span>{" "}
                Cada intento es una oportunidad para mejorar, y cada mejora te
                acerca más a una conexión real con tu hijo.
              </li>
              <li className="text-md">
                <span className="font-bold">4.</span> 📹 Haz la seña, recibe
                retroalimentación, y sigue aprendiendo con confianza.
              </li>
            </ul>
          </div>
        </section>

        <h2 className="text-md max-w-[32.563rem] font-bold mt-[2rem]">
          ¿Qué seña quieres que te evaluemos?
        </h2>

        <div className="flex flex-row items-center justify-center gap-3 mt-4">
          <div className="w-72">
            <Listbox value={selected} onChange={setSelected}>
              <div className="relative">
                <Listbox.Button className="flex border border-gray-300 px-4 py-2 rounded w-full text-left justify-between bg-[#2241A0] items-center text-white">
                  <span className="block truncate">
                    {selected ? selected.name : "Selecciona una seña"}
                  </span>
                  <span className="ml-2 pointer-events-none">
                    <img
                      src="./assets/arrow_down_2.svg"
                      alt="Abrir opciones"
                      className="h-5 w-5 text-gray-400"
                    />
                  </span>
                </Listbox.Button>
                <Listbox.Options className="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm z-20">
                  {allSigns.map((sign) => (
                    <Listbox.Option
                      key={sign.id}
                      value={sign}
                      className={({ active }) =>
                        `relative cursor-default select-none py-2 pl-10 pr-4 ${
                          active ? "bg-blue-100 text-blue-900" : "text-gray-900"
                        }`
                      }
                    >
                      {({ selected: isSelectedOption }) => (
                        <>
                          <span
                            className={`block truncate ${
                              isSelectedOption ? "font-medium" : "font-normal"
                            }`}
                          >
                            {sign.name}
                          </span>
                          {isSelectedOption && (
                            <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-blue-600">
                              ✓
                            </span>
                          )}
                        </>
                      )}
                    </Listbox.Option>
                  ))}
                </Listbox.Options>
              </div>
            </Listbox>
          </div>
        </div>

        <div className="my-3 flex flex-col items-center shadow-lg w-1/2 bg-[#2241A0] p-4 rounded-md">
          <VideoRecorder
            recording={recording}
            setRecording={setRecording}
            itemParaEvaluar={selected?.name}
            videoUrl={selected?.url_video}
          />
        </div>
      </section>
    </div>
  );
};

export default Content;
