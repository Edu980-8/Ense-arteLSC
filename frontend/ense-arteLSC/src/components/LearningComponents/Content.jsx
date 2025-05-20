import { useTheme } from "../ThemeContext";
import { useState, useEffect } from "react";
import PopUp from "../PopUp.jsx";

const Content = () => {
  const { theme } = useTheme();
  const [allSigns, setAllSigns] = useState([]); // Estado para todas las señas
  const [categorias, setCategorias] = useState([]);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState("");
  const [visible, setVisible] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [popUp, setPopUp] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/signs");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const responseBody = await response.json(); // responseBody es { data: [...] }
        console.log("Signs Data from Backend:", responseBody);

        if (responseBody && responseBody.data) {
          const signsData = responseBody.data; // Este es el array de señas/cursos
          setAllSigns(signsData); // Guarda todas las señas

          // Extraer categorías únicas
          const uniqueCategoriesMap = new Map();
          signsData.forEach(sign => {
            if (sign.category && sign.category.value && !uniqueCategoriesMap.has(sign.category.value)) {
              uniqueCategoriesMap.set(sign.category.value, {
                // Usamos el ID de la categoría del backend si está disponible y es único para el valor.
                // Si múltiples categorías pueden tener el mismo 'value' pero diferente 'id',
                // y necesitas distinguirlas, ajusta esto. Para el dropdown, 'value' suele ser la clave.
                id: sign.category.id || sign.category.value, // Fallback a value si id no está.
                value: sign.category.value
              });
            }
          });
          const extractedCategories = Array.from(uniqueCategoriesMap.values());
          setCategorias(extractedCategories);

          if (extractedCategories.length > 0) {
            setCategoriaSeleccionada(extractedCategories[0].value); // Selecciona la primera por defecto
          } else {
            setCategoriaSeleccionada(""); // o manejar si no hay categorías
          }

        } else {
          console.log("La respuesta del backend no tiene la estructura esperada (falta 'data').");
          setAllSigns([]);
          setCategorias([]);
        }
      } catch (error) {
        console.log("Error al obtener datos:", error);
        setAllSigns([]);
        setCategorias([]);
      }
    };

    fetchData();
  }, []); // El array vacío asegura que se ejecute solo una vez al montar el componente

  // Definición de cursosFiltrados
  const cursosFiltrados = allSigns.filter(curso => {
    if (!categoriaSeleccionada) {
      return false; // O true si quieres mostrar todos cuando no hay categoría seleccionada
    }
    return curso.category && curso.category.value === categoriaSeleccionada;
  });

  return (
    <div className="z-10 h-screen w-[80%] overflow-y-auto">
      {/* ... (resto de tu JSX inicial: avatar, título, lista de pasos, botón EMPIEZA AHORA) ... */}
        <section className="flex flex-col items-center justify-center">
            <section className="flex flex-row items-center gap-[40px]">
            {/* ... (avatar, título, etc.) ... */}
            <img
                className="mt-[5rem] ml-[9.125rem] max-w-[10.563rem] max-h-[13.625rem]"
                src="./assets/avatar.svg"
                alt=""
            />
            <div className="flex flex-col gap-[1.5rem]">
                <h1 className="mt-[5rem] text-[24px] max-w-[32.563rem]">
                APRENDE PASO A PASO LA LENGUA DE SEÑAS PARA{" "}
                <span className="font-bold">CONECTAR</span> DESDE EL CORAZÓN
                </h1>
                <ul className="text-[16px] max-w-[33.938rem]">
                <li className="text-md">
                    <span className="font-bold">1. Mira los videos:</span> Aprende
                    cada seña de forma visual y clara.
                </li>
                <li className="text-md">
                    <span className="font-bold">2. Repite con calma:</span> No
                    necesitas perfección, solo intención.
                </li>
                <li className="text-md">
                    <span className="font-bold">3. Practica en casa:</span> Usa las
                    señas en tus rutinas diarias con tu hijo.
                </li>
                <li className="text-md">
                    <span className="font-bold">4. Refuerza con juegos:</span>{" "}
                    Pronto descubrirás que comunicarte sin palabras también es
                    mágico.
                </li>
                </ul>
            </div>
            </section>

            <button
            className={`cursor-pointer mt-[4.188rem] bg-[${theme.buttonColor}] text-[#ffffff] px-[5.875rem] py-[1.25rem] rounded-[10px]`}
            onClick={() => setVisible(!visible)}
            >
            EMPIEZA AHORA CON TU PRIMERA SEÑA
            </button>

            {visible && (
            <div className="flex flex-row gap-[1rem] mb-[1rem] items-center">
                <p className="text-[16px] font-semibold mt-4">
                Seleccione una categoría:
                </p>
                <select
                value={categoriaSeleccionada}
                onChange={(e) => setCategoriaSeleccionada(e.target.value)}
                className="mt-[2rem] mb-[1rem] px-4 py-2 border border-gray-300 rounded-lg text-[16px] w-[300px]"
                >
                {categorias.map((cat) => (
                    <option key={cat.id} value={cat.value}> {/* Asegúrate que cat.id sea único */}
                    {cat.value}
                    </option>
                ))}
                </select>
            </div>
            )}

            {visible && (
            <ul className="mt-[2rem] mb-[2rem] flex flex-row gap-x-[3rem] gap-y-[2rem] flex-wrap items-center justify-center">
                {cursosFiltrados.map((curso) => (
                <li
                    key={curso.id} // El 'id' del curso/seña
                    className={`flex flex-col items-center h-[353px] w-[312px] bg-[${theme.buttonColor}] rounded-b-[10px] pb-[1rem]`}
                >
                    <iframe
                    // Deberías usar la URL del video del curso: curso.url_video
                    src={curso.url_video }
                    className="w-full h-[232px] pt-1 px-1"
                    title={`Video de ${curso.name}`} // Buena práctica añadir título al iframe
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                    ></iframe>
                    <h2 className="text-[34px] mt-[4px] mb-[9px] font-bold text-[#ffffff]">
                    {curso.name} {/* Asumiendo que 'name' es el título del curso/seña */}
                    </h2>
                    <div className="relative flex flex-row items-center gap-[0.5rem]">
                    <button
                        className="relative bg-[#b9e185] text-[#000000] pl-[18.37px] py-[10px] pr-[37px] rounded-[10px]"
                        onClick={() => {
                        setSelectedCourse(curso);
                        setPopUp(true);
                        }}
                    >
                        Inténtalo Tú!
                    </button>
                    <img
                        className="w-[20px] h-[20px] absolute justify-end right-2 z-40"
                        // La respuesta del backend tiene 'curso.category.medal_image_url'.
                        // Si cada curso tiene su propia imagen, el backend debe proveerla.
                        // Si es la imagen de la medalla de la categoría:
                        src={ "./public/assets/mano_azul.svg"} // Usa la URL de la medalla o un fallback
                        alt={`Medalla de ${curso.category?.value}`}
                    />
                    {/* PopUp se renderiza condicionalmente aquí, lo cual es correcto para un solo PopUp */}
                    </div>
                </li>
                ))}
            </ul>
            )}
            {/* Renderiza el PopUp aquí si solo debe haber una instancia y se controla su visibilidad */}
            {popUp && selectedCourse && (
                <PopUp
                    setPopUp={setPopUp}
                    curso={selectedCourse}
                    setSelectedCourse={setSelectedCourse} // Asegúrate que PopUp usa esto si necesita limpiar el curso seleccionado
                />
            )}
        </section>
    </div>
  );
};

export default Content;