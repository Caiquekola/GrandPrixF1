import { useEffect, useState } from "react";

function Cars() {
    const [cars, setCars] = useState([]);
    const [race, setRace] = useState({ current_lap: 0, total_laps: 71, sim_time_hms: "00:00:00" });

    const handleGet = async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/carros");
            const data = await response.json();

            // Aceita os dois formatos:
            // 1) Antigo: [ ...carros ]
            // 2) Novo: { race: {...}, leaderboard: [...] }
            let leaderboard = [];
            let raceData = { current_lap: 0, total_laps: 71, sim_time_hms: "00:00:00" };

            if (Array.isArray(data)) {
                leaderboard = data;

                // Se não vier "race", calcula a volta atual pelo array
                const maxLap = leaderboard.length
                    ? Math.max(...leaderboard.map(c => Number(c.current_lap ?? 0)))
                    : 0;

                raceData = {
                    ...raceData,
                    current_lap: maxLap,
                };
            } else {
                leaderboard = Array.isArray(data.leaderboard) ? data.leaderboard : [];
                raceData = data.race ? { ...raceData, ...data.race } : raceData;

                // fallback: se race.current_lap vier vazio, calcula pelo leaderboard
                if (!raceData.current_lap && leaderboard.length) {
                    raceData.current_lap = Math.max(...leaderboard.map(c => Number(c.current_lap ?? 0)));
                }
            }

            // Ordena pela posição (1º, 2º, 3º...) vinda do Backend
            const sortedCars = leaderboard.sort((a, b) => a.position - b.position);

            setRace(raceData);
            setCars(sortedCars);
        } catch (error) {
            console.error("Erro ao buscar classificação:", error);
        }
    };

    useEffect(() => {
        handleGet();
        const interval = setInterval(handleGet, 2000); // Polling a cada 2s
        return () => clearInterval(interval);
    }, []);

    return (
        <div style={{ width: "100%", padding: "3rem 0", display: "flex", justifyContent: "center" }}>
            <div style={{ width: "80%", display: "flex", flexDirection: "column", gap: "2rem" }}>
                <h1 style={{ textAlign: "center", color: "#000000ff", textTransform: "uppercase", letterSpacing: "2px" }}>
                    Classificação em Tempo Real
                </h1>

                {/* ADIÇÃO: volta atual/total + tempo simulado (sem mudar a estilização existente) */}
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div style={{ fontWeight: 700, color: "#000000ff", textTransform: "uppercase", letterSpacing: "1px" }}>
                        Volta atual: {race.current_lap}/{race.total_laps}
                    </div>

                    <div style={{ fontWeight: 700, color: "#000000ff", textTransform: "uppercase", letterSpacing: "1px" }}>
                        Tempo de corrida: {race.sim_time_hms}
                    </div>
                </div>

                <div style={{ backgroundColor: "#1e1e1e", padding: "2rem", borderRadius: 12, boxShadow: "0 10px 30px rgba(0,0,0,0.5)" }}>
                    <table style={{ width: "100%", borderCollapse: "collapse" }}>
                        <thead>
                            <tr>
                                <th style={{ ...th, width: "10%" }}>Pos</th>
                                <th style={{ ...th, width: "40%" }}>Piloto</th>
                                <th style={{ ...th, width: "30%" }}>Equipe</th>
                                <th style={{ ...th, textAlign: "right", width: "20%" }}>Nº Carro</th>
                            </tr>
                        </thead>

                        <tbody>
                            {Array.isArray(cars) && cars.map((item) => (
                                <tr key={item.id || item.car_number} style={trHover}>
                                    <td style={{ ...td, color: item.position <= 3 ? "#FFD700" : "#FFF" }}>
                                        {item.position}º
                                    </td>
                                    <td style={td}>{item.driver}</td>
                                    <td style={td}>{item.team}</td>
                                    <td style={{ ...td, textAlign: "right" }}>
                                        <span style={badge}>{item.car_number}</span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

// Estilização mantida conforme solicitado
const th = {
    borderBottom: "2px solid #606066",
    padding: "16px 10px",
    color: "#AAAAAA",
    textTransform: "uppercase",
    textAlign: "left",
};

const td = {
    borderBottom: "1px solid #303037",
    padding: "16px 10px",
    fontWeight: 600,
    color: "#FFF",
};

const trHover = {
    transition: "background 0.3s ease",
};

const badge = {
    backgroundColor: "#e10600",
    padding: "4px 12px",
    borderRadius: "4px",
    fontSize: "0.85rem",
    fontWeight: "bold",
    color: "#FFF"
};

export default Cars;
