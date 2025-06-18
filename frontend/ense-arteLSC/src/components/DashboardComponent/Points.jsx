import React from "react";

const users = [
  {
    username: "LeidySignQueen",
    level: 7,
    xp: 480,
    nextLevelXp: 600,
    medals: 8,
    totalPoints: 1600,
  },
  {
    username: "EduardTheSignMaster",
    level: 6,
    xp: 410,
    nextLevelXp: 550,
    medals: 7,
    totalPoints: 1450,
  },
  {
    username: "DanielGestureGuru",
    level: 5,
    xp: 390,
    nextLevelXp: 500,
    medals: 6,
    totalPoints: 1320,
  },
  {
    username: "LauraSignsFast",
    level: 4,
    xp: 290,
    nextLevelXp: 400,
    medals: 4,
    totalPoints: 950,
  },
  {
    username: "AndresExpress",
    level: 5,
    xp: 330,
    nextLevelXp: 480,
    medals: 5,
    totalPoints: 1100,
  },
  {
    username: "ValentinaVision",
    level: 3,
    xp: 210,
    nextLevelXp: 300,
    medals: 3,
    totalPoints: 800,
  },
  {
    username: "MateoHandsOn",
    level: 2,
    xp: 160,
    nextLevelXp: 250,
    medals: 2,
    totalPoints: 670,
  },
  {
    username: "SantiSignsAllDay",
    level: 4,
    xp: 270,
    nextLevelXp: 400,
    medals: 4,
    totalPoints: 890,
  },
  {
    username: "AnaSignalSpark",
    level: 3,
    xp: 190,
    nextLevelXp: 300,
    medals: 2,
    totalPoints: 720,
  },
];


const Points = () => {
  return (
    <div className="min-h-screen px-6 py-10 bg-white text-black flex flex-col items-center  mx-auto">
      <h1 className="text-3xl font-bold mb-8 text-[#2241A0] text-center">
        🏅 Ranking de Jugadores
      </h1>

      <div className="w-full max-w-5xl shadow rounded-xl border border-[#b9e185] overflow-hidden">
        <table className="min-w-full text-sm text-left">
          <thead className="bg-[#2241A0] text-white font-semibold text-xs uppercase text-center">
            <tr>
              <th className="px-4 py-3">Jugador</th>
              <th className="px-4 py-3">Nivel</th>
              <th className="px-4 py-3">XP</th>
              <th className="px-4 py-3">Progreso</th>
              <th className="px-4 py-3">Medallas</th>
              <th className="px-4 py-3 text-right">Puntos</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user, i) => {
              const progress = (user.xp / user.nextLevelXp) * 100;

              return (
                <tr
                  key={i}
                  className="border-t border-[#e2e8f0] hover:bg-[#f9fafb] transition"
                >
                  <td className="px-4 py-3 font-medium">{user.username}</td>
                  <td className="px-4 py-3">{user.level}</td>
                  <td className="px-4 py-3">
                    {user.xp} / {user.nextLevelXp}
                  </td>
                  <td className="px-4 py-3 w-48">
                    <div className="bg-[#e5e7eb] h-2 rounded-full overflow-hidden">
                      <div
                        className="h-2 rounded-full bg-[#b9e185]"
                        style={{ width: `${progress}%` }}
                      />
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    {Array.from({ length: user.medals })
                      .map((_, j) => "🥇")
                      .join(" ")}
                  </td>
                  <td className="px-4 py-3 text-right font-bold text-[#2241A0]">
                    {user.totalPoints}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Points;
