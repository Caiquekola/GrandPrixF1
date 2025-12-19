import './App.css'
import { BrowserRouter, Routes, Route, Outlet, Navigate } from 'react-router-dom';
import Header from './components/header';
import Nav from './components/nav';
import Cars from './components/cars';
import Dashboard from './components/dashboard';
function App() {

  function Body() {
    return (
      <main className={"main"}>
        <Header />
        <div className="container">
          <Nav />
          <Outlet />
        </div>
      </main>
    );
  }

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path='' element={<Body />}>
            <Route index element={<Navigate to="carros" />} />
            <Route path='carros' element={<Cars />} />
            <Route path='interface' element={<Dashboard />} />
          </Route>
        </Routes>
      </BrowserRouter >
    </>
  )
}

export default App
