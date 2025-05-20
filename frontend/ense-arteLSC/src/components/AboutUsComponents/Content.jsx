import React, { useState } from "react";
const Content = () => {
  const [creators, setCreators] = useState([
    { id: 1, name: "Eduard", img: "./assets/Eduard_Avatar.svg",description:"Encargado de la estética de la aplicación y del Modelo IA. Ing. Electrónico y desarrolador FullStack. " },
    { id: 2, name: "Leidy", img: "./assets/Leidy_Avatar.svg",description:"Encargada de la organizacion del proyecto y del Modelo IA. Ing. de Sistemas y administradora de Plataformas de IBM." },
    { id: 3, name: "Daniel", img: "./assets/Daniel_Avatar.svg",description:"Encargado de la lógica de la aplicación y del Modelo IA. Ing. Físico  y desarrolador FullStack." },
  ]);
  const isOdd = (index) => index % 2 === 1; 
  return (
    <div className="flex flex-col gap-4 mx-auto justify-center ">
      <h1 className="text-[28px] text-center w-[780px] mb-60 uppercase font-medium">Derribar barreras, construir puentes con la ayuda de nuestros amigos IA</h1>
      <ul className="relative flex flex-row gap-[48px] ">
        {creators.map((creator, index) => (
          <div
            key={creator.id}
            className={isOdd(index) ? ` flex flex-col gap-4 w-[247px] h-[226px] bg-[#2241A0] mt-10 rounded-[25px] items-center ` : ` flex flex-col gap-4 w-[247px] h-[226px]  bg-[#2241A0]  rounded-[25px] items-center `}
          >
            <img
              className={isOdd(index)? " absolute -top-30 w-[226px] h-[248px] mx-auto " : " absolute -top-40 w-[226px] h-[248px] mx-auto  "}
              src={creator.img}
            ></img>
            <li
              key={creator.id}
              className=" mt-20 pt-4 text-white text-[20px] w-[226px]  text-center "
            >
              {creator.name}
            </li>
            <p className="text-[11px] text-center  w-[220px] text-white">{creator.description}</p>
          </div>
        ))}
      </ul>
      <p className="text-[15px] text-center mt-4 w-[780px]">
        Detrás de este proyecto hay un equipo humano apasionado y tres pequeños
        grandes aliados que te acompañarán en el camino: nuestros robots IA
        diseñados para hacer del aprendizaje en lenguaje de señas una
        experiencia divertida, cercana y llena de amor. Ellos te guiarán paso a
        paso para que comunicarte con tu hijo sea algo natural y lleno de magia.
        Porque creemos que todos merecen ser escuchados, vistos y amados, sin
        importar las palabras
      </p>
    </div>
  );
};

export default Content;
