function Header() {
    // Defina a altura do header aqui para facilitar ajustes
    const headerHeight = "80px"; 

    return (
        <>
            <header style={{
                backgroundColor: "#15151E",
                position: 'fixed',
                top: 0,
                width: "100%",
                height: headerHeight, 
                display: "flex",
                zIndex: 5,
                justifyContent: "center",
                borderBottom: "1px solid #303037",
                alignItems: "center",
                padding: "5px",
                 // Removi o padding para a imagem e o texto ocuparem tudo
            }}>
                <div style={{ width: "100%", height: "100%", position: "relative",alignContent:"center", display:"flex",alignItems:"center",justifyContent:"center" }}>
                    {/* Imagem de Fundo */}
                    <img
                        src="https://guiadosesportes.com/wp-content/uploads/2024/12/image-596.png"
                        alt="logo"
                        style={{
                            width: "70%",
                            height: "100%",
                            objectFit: "cover",
                            objectPosition: "center",
                            opacity: "30%", // A imagem fica mais escura para o texto aparecer
                            display: "block",
                            borderRadius: "12px"
                        }}
                    />
                    
                    {/* Texto Sobreposto */}
                    <h1 style={{
                        position: "absolute", // Faz o texto flutuar
                        top: "50%",           // Centraliza verticalmente
                        left: "50%",          // Centraliza horizontalmente
                        transform: "translate(-50%, -50%)", // Ajuste fino da centralização
                        color: "#FFFFFF",     // Cor branca
                        margin: 0,            // Remove margens padrão do h1
                        fontSize: "24px",     // Tamanho da fonte
                        fontWeight: "bold",
                        textAlign: "center",
                        width: "100%",        // Garante que o texto centralize mesmo se for longo
                        textTransform: "uppercase", // Garante letras maiúsculas
                        zIndex: 10            // Garante que fique acima da imagem
                    }}>
                        GP BRASIL - ED. FUTEBOL 
                    </h1>
                </div>
            </header>
            
            {/* Espaçador */}
            <div style={{ height: headerHeight }}></div>
        </>
    )
}

export default Header