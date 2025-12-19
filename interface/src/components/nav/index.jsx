import { Link } from 'react-router-dom';
import styles from "./nav.module.css";

function Nav() {
    return (
        <>
            <nav className={styles.navContainer}>
                <div style={{ width: "85%", padding: "0px 24px", display: "flex", alignItems: "center",justifyContent:"center" }}>
                    <Link to='/carros' style={{ padding: "8px 24px" }}>Carros</Link>
                    <Link to='/interface' style={{ padding: "8px 24px" }}>Interface</Link>
                </div>
            </nav>
        </>
    )
}

export default Nav