import { useTheme } from "./ThemeContext";
import { useNavigate, useLocation } from "react-router-dom";
import { logout } from "../../utils/auth";

const secciones = [
  { nombre: "Aprende Señas", icono: "mano_amarilla", path: "/learn" },
  { nombre: "Evalua tu seña", icono: "mano_verde", path: "/practice" },
  { nombre: "Conócenos", icono: "mano_amarilla", path: "/about" },
  {nombre: "Puntuaciones", icono: "mano_verde", path: "/scores"},
  { nombre: "Cerrar Sesión", icono: "cerrar-sesion", path: "/" },
];

const isOdd = (number) => number % 2 !== 0;

const VerticalNavBar = () => {
  const navigate = useNavigate();
  const location = useLocation(); // Obtén la ruta actual
  const { theme } = useTheme();

  const handleLogout = () => {
    logout();
    navigate("/login"); // Redirige al login
  };

  return (
    <div
      className={`flex flex-col items-center gap-[6.438rem] w-[22.813rem] bg-[${theme.buttonColor}] h-[100svh]`}
    >
      <img
        className="w-[259px] h-[85px] left-0 mx-[2rem] mt-[4.375rem] cursor-pointer"
        src="./assets/Logo2_DarkMode.svg"
        alt=""
        onClick={() => navigate("/")}
      />
      <div className="flex flex-col justify-between items-left">
        <ul className="flex flex-col gap-4 justify-center">
          {secciones.map((seccion, index) => {
            const isActive = location.pathname === seccion.path;
            const color = isOdd(index) ? "#B9E185" : "#FFC410"; // El color dinámico

            return (
              <li
                key={index}
                onClick={() => navigate(seccion.path)}
                className={`flex flex-row items-center gap-2 mb-4 cursor-pointer 
                  ${isActive ? "font-bold underline underline-offset-8" : "hover:underline hover:underline-offset-8"}`}
                style={{
                  textDecorationColor: isActive ? color : "transparent", // Aplica el color de subrayado solo si es activo
                }}
              >
                <img
                  src={`./assets/${seccion.icono=="cerrar-sesion" ? "cerrar-sesion.png" : seccion.icono+".svg"}`}
                  alt={seccion.nombre}
                  className="size-[40px]"
                  onClick={seccion.nombre == "Cerrar Sesión" ? handleLogout : () => navigate(seccion.path)}
                />
                <span className="text-[#ffffff]">{seccion.nombre}</span>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
};

export default VerticalNavBar;
