import HorizontalNavBar from "../components/HorizontalNavBar";
import { useTheme } from "../components/ThemeContext";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const { theme } = useTheme();
  const navigate = useNavigate();
  return (
    <div
      className="w-full px-[7.68rem] pt-[3.375rem] h-[100svh] "
      style={{ backgroundColor: theme.backgroundColor }}
    >
      <HorizontalNavBar />

      <div className="max-h-[80svh] grid grid-cols-2 justify-center items-center h-full gap-16">
        <div>
          <h1
            className="text-[2.5rem] font-poppins text-black"
            style={{ color: theme.textColor }}
          >
            EL LENGUAJE DEL AMOR NO SIEMPRE SE ESCUCHA,{" "}
            <span className="font-bold">¡A VECES SE SIENTE!</span>
          </h1>
          <p
            className="text-[1.125rem] font-normal font-poppins text-black"
            style={{ color: theme.textColor }}
          >
            Acompáñanos en este viaje para aprender a comunicarte con tu hijo de
            una forma única y especial.
          </p>
          <div className="flex flex-col gap-[1.563rem] mt-[4.625rem]">
            <button
              className="w-[27.125rem] rounded-[0.625rem] text-white py-[0.75rem] px-[1.25rem] drop-shadow-lg cursor-pointer"
              style={{
                backgroundColor: theme.buttonColor,
                color: theme.textButtonColor,
              }}
              onClick={() => navigate("/login")}
            >
              EMPIEZA A APRENDER
            </button>

            <button
              className="w-[27.125rem] rounded-[0.625rem] bg-white text-[#2241A0] border border-[#2241A0] py-[0.75rem] px-[1.25rem] cursor-pointer"
              style={{
                backgroundColor: theme.secondaryButtonColor,
                color: theme.secondaryTextButtonColor,
                borderColor: theme.secondaryTextButtonColor,
              }}
              onClick={() => navigate("/login")}
            >
              YA TENGO UNA CUENTA
            </button>
          </div>
        </div>

        <div className="flex justify-center items-center w-[661px] h-[491px]">
          <video
            className="w-full h-full rounded-lg shadow-lg"
            controls
            autoPlay
            muted
            loop
          >
            <source
              src="https://drive.google.com/uc?export=download&id=1sH8KvPM-RFcIB168iaWWLAOX6xCPeQku"
              type="video/mp4"
            />
            Tu navegador no soporta el elemento de video.
          </video>
        </div>
      </div>
    </div>
  );
};

export default Home;
