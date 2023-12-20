import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Home() {
  const [heros, setHeros] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/heroes")
      .then((r) => r.json())
      .then(setHeros);
  }, []);

  return (
    <section>
      <h2>All Heroes</h2>
      <ul>
        {heros.map((hero) => (
          <li key={hero.id}>
            <Link to={`http://127.0.0.1:5555/heroes/${hero.id}`}>{hero.super_name}</Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default Home;
