export default function App() {
  return (
    <main className="bg-base-100 h-screen w-screen flex flex-col items-center justify-center gap-4 md:gap-6">
      <h1 className="font-semibold text-6xl mb-1 md:text-7xl">Lyricsman.</h1>
      <p className="w-[28rem] text-center text-base-content/70 max-sm:w-[23rem] md:text-xl md:w-[30rem]">Get the lyrics of Your favorite songs from spotify, in real-time. even the unavailable ones.</p>
      <a className="btn btn-neutral text-lg md:text-xl md:py-6" href="https://spotifylyrics-six.vercel.app/auth/login" target="_blank">Connect Your Spotify</a>
      <footer>
        <p className="text-sm text-center md:text-lg">Made with ❤️ by <a href="https://www.google.com/" target="_blank">keishz.</a></p>
      </footer>
    </main>
  );
}
