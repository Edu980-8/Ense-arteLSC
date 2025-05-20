import ToggleButton from "./ToggleButton";
import { useTheme } from "./ThemeContext";
import { useNavigate } from "react-router-dom";


const HorizontalNavBar = () => {
  const navigate = useNavigate();
  
  const { theme } = useTheme();
  return (
    <div
      className="flex flex-row justify-between items-center"
      style={{ backgroundColor: theme.backgroundColor }}
    >
      <img
        className="w-[212px] h-[70px] left-0 cursor-pointer  "
        src={
          theme.backgroundColor === "#ffffff"
            ? "./assets/Logo2.svg"
            : "./assets/Logo2_DarkMode.svg"
        }
        alt=""
        onClick={() => navigate("/")}
      />

      <div
        className="flex flex-row gap-[2.375rem] items-center text-black/25 font-semibold font-poppins "
        style={{ color: theme.textColor }}
      >
        <ul
          className=""
          style={{
            color: theme.textColor,
            opacity: theme.backgroundColor === "#ffffff" ? "0.5" : "1",
          }}
        >
          <div className="flex flex-row gap-[0.625rem] items-center">
            <li className="cursor-pointer">Lengua de señas </li>
            <img
             className="cursor-pointer"
              src={
                theme.backgroundColor === "#ffffff"
                  ? "./assets/Arrow_Down.svg"
                  : "./assets/Arrow_Down_Dark.svg"
              }
              alt=""
            />
          </div>
        </ul>

        <ToggleButton />

        <img
          src={
            theme.backgroundColor === "#ffffff"
              ? "./assets/Configure.svg"
              : "./assets/Config_Dark_Mode.svg"
          }
          className="size-8"
          alt=""
        />
      </div>
    </div>
  );
};

export default HorizontalNavBar;
