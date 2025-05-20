import { useState } from "react";
import { useNavigate } from "react-router-dom";
const Login = () => {
  const [mode, setMode] = useState("login");
  const navigate = useNavigate();
  return (
    <div className="flex flex-col justify-center items-center gap-[41px] mt-[100px] ">
      <img
        className="w-[200px] h-[73px] cursor-pointer"
        src="./assets/Logo2.svg"
        alt=""
        onClick={() => navigate("/")}
      />

      <ul className="flex flex-row  text-center justify-center items-center gap-[41px]">
        <li
          className={`text-[#2241A0] border-b-[#2241A0] cursor-pointer ${
            mode === "login" ? "border-b-[1px] pb-1" : ""
          } `}
          onClick={() => setMode("login")}
        >
          INICIO SESIÓN
        </li>
        <li
          className={`text-[#2241A0] border-b-[#2241A0] cursor-pointer ${
            mode === "register" ? "border-b-[1px] pb-1" : ""
          } `}
          onClick={() => setMode("register")}
        >
          REGISTRARSE
        </li>
      </ul>

      {/* <div className="flex flex-row justify-center items-center gap-[41px]">
        <img
          className="size-[48px] rounded-full cursor-pointer border-[#2241A0] border-[1px] p-2 "
          src="./assets/Frame-1.svg"
          alt=""
        />
        <img
          className="size-[48px] rounded-full cursor-pointer border-[#2241A0] border-[1px] p-2"
          src="./assets/Frame-2.svg"
          alt=""
        />
        <img
          className="size-[48px] rounded-full cursor-pointer border-[#2241A0] border-[1px] p-2"
          src="./assets/Frame.svg"
          alt=""
        />
      </div> */}

      {mode === "login" ? (
        <div className="flex flex-col gap-[25px]">
          <div>
            <input
              type="text"
              placeholder="Email"
              className="border-b-[#2241A0] border-b-[1px] pb-2 focus:outline-none"
            />
            <img src="" alt="" />
          </div>

          <div>
            <input
              type="password"
              placeholder="Password"
              className="border-b-[#2241A0] border-b-[1px] pb-2 focus:outline-none"
            />
            <img src="" alt="" />
          </div>
        </div>
      ) : (
        <div className="flex flex-col gap-[25px]">
          <div>
            <input
              type="text"
              placeholder="Nombre"
              className="border-b-[#2241A0] border-b-[1px] pb-2 focus:outline-none"
            />
            <img src="" alt="" />
          </div>

          <div>
            <input
              type="text"
              placeholder="Email"
              className="border-b-[#2241A0] border-b-[1px] pb-2 focus:outline-none"
            />
            <img src="" alt="" />
          </div>

          <div>
            <input
              type="password"
              placeholder="Contraseña"
              className="border-b-[#2241A0] border-b-[1px] pb-2 focus:outline-none"
            />
            <img src="" alt="" />
          </div>
        </div>
      )}

      <div>
        <p className="text-[#2241A0] cursor-pointer">¿Olvidaste tu contrasena?</p>
      </div>

      <button className="bg-[#2241A0] text-white text-[1rem] rounded-[5px] py-[1rem] px-[48px] cursor-pointer"
        onClick={() => navigate("/learn")}>
        {mode === "login" ? "INICIAR SESIÓN" : "REGISTRARSE"} 
      </button>
    </div>
  );
};

export default Login;
