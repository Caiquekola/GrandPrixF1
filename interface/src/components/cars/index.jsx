import { useEffect, useState } from "react";

function Cars() {
    const [cars, setCars] = useState([]);

    const handleGet = async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/carros");
            const data = await response.json();
            setCars(data)

        } catch (error) {
            console.error("Erro ao buscar:", error);
        }
    }

    useEffect(() => {
        handleGet()
    }, [])

    return (
        <div style={{ width: "100%", padding: "3rem 0", display: "flex", justifyContent: "center", }}>
            <div style={{ width: "80%", display: "flex", flexDirection: "column", gap: "3rem" }}>
                <h1>Carros classificados</h1>

                <div style={{ backgroundColor: "#000", padding: "3.5rem 4rem", borderRadius: 10 }}>
                    <table style={{ width: "100%", borderCollapse: "collapse" }}>
                        <thead>
                            <tr>
                                <th style={{ ...th, width: "40%" }}>Carro</th>
                                <th style={{ ...th, width: "20%" }}>Nacionalidade</th>
                                <th style={{ ...th, width: "25%" }}>Equipe</th>
                                <th style={{ ...th, textAlign: "right", padding: "16px 4px 16px 48px" }}>N. Carro</th>
                            </tr>
                        </thead>

                        <tbody>
                            {cars.map((item, index) => (
                                <tr key={index}>
                                    <td style={td}>{item.driver}</td>
                                    <td style={{ ...td, textTransform: "uppercase" }}>{item.country}</td>
                                    <td style={td}>{item.team}</td>
                                    <td style={{ ...td, textAlign: "right", padding: "16px 4px 16px 48px" }}>{item.car_number}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}

const th = {
    borderBottom: "2px solid #606066",
    padding: "16px 48px 16px 4px",
    color: "#AAAAAA",
    textTransform: "uppercase",
    textAlign: "left",
};

const td = {
    borderBottom: "1px solid #303037",
    padding: "16px 48px 16px 4px",
    fontWeight: 600,
    color: "#FFF",
    padding: "10px",
};
export default Cars