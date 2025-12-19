import { useEffect, useState } from "react";
import styles from "./dashboard.module.css"

function Dashboard() {
    const [cars, setCars] = useState([]);
    const [selectTeams, setSelectTeams] = useState("Red Bull");
    const [selectIsccp, setSelectIsccps] = useState("01");
    const teams = [
        "Red Bull",
        "Ferrari",
        "McLaren",
        "Mercedes",
        "Aston Martin",
        "Alpine",
        "Williams",
        "Haas",
        "Racing Bulls",
        "Sauber",
        "Lotus",
        "Renault"
    ];

    const handleGet = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/dashboard?team=${selectTeams}&sector=${selectIsccp}`);
            const data = await response.json();
            console.log(data)
            setCars(data)

        } catch (error) {
            console.error("Erro ao buscar:", error);
        }
    }

    const selectItem = (e) => {
        setSelectIsccps(e)
    }
    useEffect(() => {
        const interval = setInterval(() => {
            handleGet()
            console.log(selectIsccp);
        }, 2000)

        return () => {
            clearInterval(interval)
        }
    }, [selectTeams, selectIsccp])

    return (
        <div className={styles.dashboard_container}>
            <div className={styles.dashboard_title}>
                <h1>Estado dos Pneus</h1>
            </div>

            <div className={styles.dashboard_team}>
                <ul style={{ width: "80%" }}>
                    {window.innerWidth > 1440 ? (
                        teams.map((team, index) => (
                            <li key={index}>
                                <button onClick={() => setSelectTeams(team)}>
                                    {team}
                                </button>
                            </li>
                        ))
                    ) :
                        (
                            <select onChange={(e) => setSelectTeams(e.target.value)} className={styles.dashboard_select_team}>
                                {teams.map((team, index) => (
                                    <option key={index} value={team}>
                                        {team}
                                    </option>
                                ))}
                            </select>
                        )}
                </ul>
            </div>

            <div style={{ width: "80%", display: "flex", flexDirection: "column" }}>
                <div className={styles.dashboard_table_container}>
                    <select onChange={(e) => selectItem(e.target.value)} className={styles.dashboard_select}>
                        {Array.from({ length: 15 }, (_, i) => (i + 1).toString().padStart(2, "0")).map((num) => (
                            <option key={num} value={num}>
                                ISCCP {num}
                            </option>
                        ))}
                    </select>

                    {cars.map((car, carIndex) => (

                        <div key={carIndex} style={{ marginBottom: "2rem" }}>
                            <div className={styles.dashboard_table_pilot}>
                                <p style={{ fontWeight: "bold", fontSize: "1.2rem", marginBottom: "0.5rem" }}>
                                    {car.driver}
                                </p>
                                <p style={{ fontWeight: "bold", fontSize: "1.2rem", marginBottom: "0.5rem" }}>
                                    Volta atual: {car.tire_readings[0]?.lapNumber}
                                </p>
                            </div>
                            <table className={styles.dashboard_table} >
                                <thead>
                                    <tr>
                                        <th>Pneu</th>
                                        <th>Composição</th>
                                        <th>Pressão</th>
                                        <th>Temperatura</th>
                                        <th style={{ textAlign: "right", padding: "16px 4px 16px 48px" }}>Desgaste</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {car.tire_readings.map((reading, readIndex) =>
                                        Object.entries(reading.tireData).map(([tireName, tireInfo]) => (
                                            <tr key={`${carIndex}-${readIndex}-${tireName}`}>
                                                <td >{tireName}</td>
                                                <td style={{ textTransform: "uppercase" }}>{tireInfo.compound}</td>
                                                <td >{tireInfo.pressure}</td>
                                                <td >{tireInfo.temperature}</td>
                                                <td style={{ textAlign: "right", padding: "16px 4px 16px 48px" }}>{tireInfo.wear}%</td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>
                    ))}


                </div>
            </div>
        </div>
    )
}


export default Dashboard