import { Link } from 'react-router-dom';
import styles from "./nav.module.css";

function Nav() {
    return (
        <>
            <nav className={styles.navContainer}>
                <div className={styles.navImg}>       
                <img src="https://media.formula1.com/image/upload/c_lfill,w_3392/q_auto/v1740000000/fom-website/manual/Misc/Red%20Box%20Image.webp" alt="" 
                    style={{ objectFit: "cover", borderRadius: 10}}/>
                <span></span>
                <h1>Monitor GP - São Paulo</h1>
                </div>
                <div style={{ width: "85%", padding: "0px 24px", backgroundColor: "#000", display: "flex", alignItems: "center" }}>
                    <p style={{ marginLeft: "26px" }} >2025</p>
                    <Link to='/cars' style={{ padding: "8px 24px" }}>Pilotos</Link>
                    <Link to='/dashboard' style={{ padding: "8px 24px" }}>Dashboard</Link>
                </div>
            </nav>
        </>
    )
}

export default Nav