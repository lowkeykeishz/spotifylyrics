import ky from "ky";

export default function App() {

  const handleLogin = async () => {
    const response = await ky.get("https://spotifylyrics-six.vercel.app/auth/login");
    console.log(response);
  };
  return (
    <main className="bg-base-100 h-screen w-screen flex flex-col items-center justify-center gap-4 md:gap-6">
      <h1 className="font-semibold text-6xl mb-1 md:text-7xl">Lyricsman.</h1>
      <p className="w-[28rem] text-center text-base-content/70 max-sm:w-[23rem] md:text-xl md:w-[30rem]">Get the lyrics of Your favorite songs from spotify, in real-time. even the unavailable ones.</p>
      <button className="btn btn-neutral text-lg md:text-xl md:py-6" onClick={handleLogin}>Connect Your Spotify</button>
      <footer>
        <p className="text-sm text-center md:text-lg">Made with ❤️ by <a href="https://www.google.com/" target="_blank">keishz.</a></p>
      </footer>
    </main>
  );
}
