
function Header() {
    return (
        <>
            <header style={{ backgroundColor: "#15151E", position: 'fixed', top: 0, width: "100%", display: "flex", zIndex: 5, justifyContent: "center", borderBottom: "1px solid #303037", alignItems: "center", padding: "22px 0" }}>
                <div style={{ width: "85%" }}>
                    <img
                        src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/F1.svg/1024px-F1.svg.png" alt="logo"
                        style={{ width: 96, background: "transparent", objectFit: "cover" }} />
                </div>
            </header>
        </>
    )
}

export default Header