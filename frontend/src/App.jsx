import { useState } from "react";
import {
  ArrowRight,
  Check,
  ClipboardPenLine,
  FileDown,
  UsersRound,
} from "lucide-react";

const features = [
  {
    number: "01",
    icon: ClipboardPenLine,
    title: "Make every plan feel personal.",
    text: "Tune exercises around your patient's goals, abilities, and life. Change reps, frequency, and instructions without starting over.",
    accent: "blue-band",
    label: "Your plan, your way",
  },
  {
    number: "02",
    icon: UsersRound,
    title: "Bring your best thinking together.",
    text: "Share what works with other therapists, discover new ideas, and keep the care conversation moving between visits.",
    accent: "sun-band",
    label: "Your community, connected",
  },
  {
    number: "03",
    icon: FileDown,
    title: "Keep progress within reach.",
    text: "Give your patient a clear digital plan or print a polished PDF when a download is not the right fit for their routine.",
    accent: "sky-band",
    label: "Your patient's next step",
  },
];

function App() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setStatus("loading");
    setError("");

    try {
      const response = await fetch("/api/v1/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const responseText = await response.text();
      let payload = {};
      if (responseText) {
        try {
          payload = JSON.parse(responseText);
        } catch {
          payload = {};
        }
      }
      if (!response.ok) {
        throw new Error(
          payload.detail || "We could not reach FlexHEP. Please try again.",
        );
      }
      setStatus("success");
    } catch (submitError) {
      setError(submitError.message);
      setStatus("error");
    }
  }

  return (
    <main>
      <section className="hero-banner">
        <img
          className="hero-photo"
          src="/assets/flexhep-hero.png"
          alt="Woman stretching on a blue exercise mat at home"
          onError={(event) => {
            event.currentTarget.src =
              "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=1800&q=85";
          }}
        />
        <div className="photo-shade" />
        <div className="light-beam beam-one" />
        <div className="light-beam beam-two" />
        <div className="light-beam beam-three" />
        <div className="hero-content">
          <h1>Healing <span>in Process...</span></h1>
          {status === "success" ? (
            <div className="hero-success" role="status">
              <span className="success-check"><Check size={17} /></span>
              <span>You&apos;re on the list.</span>
            </div>
          ) : (
            <form className="hero-form" onSubmit={handleSubmit}>
              <label className="email-prompt" htmlFor="email">Give me updates when the app launches</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="Your email address"
                required
                aria-describedby={error ? "form-error" : undefined}
              />
              <button type="submit" disabled={status === "loading"}>
                {status === "loading" ? "Joining..." : "Keep me posted"}
                <ArrowRight size={17} />
              </button>
              {error && <span className="form-error" id="form-error" role="alert">{error}</span>}
            </form>
          )}
        </div>
      </section>

      <section className="intro-strip">
        <p>FlexHEP is the flexible home exercise space for physical therapists and the people they care for.</p>
      </section>

      <section className="information-sections" aria-label="FlexHEP benefits">
        {features.map(({ number, icon: Icon, title, text, accent, label }, index) => (
          <article className={`info-band ${accent}`} key={number}>
            <div className="info-inner">
              <div className="info-index"><span>{number}</span><span className="index-rule" /></div>
              <div className="info-copy">
                <div className="info-label"><Icon size={17} /> {label}</div>
                <h2>{title}</h2>
                <p>{text}</p>
              </div>
              <div className={`band-shape shape-${index + 1}`} aria-hidden="true"><span>{number}</span></div>
            </div>
          </article>
        ))}
      </section>

      <footer className="site-footer">
        <span className="footer-mark">F</span>
        <span>FlexHEP</span>
        <span className="footer-note">Home exercise, with more humanity.</span>
      </footer>
    </main>
  );
}

export default App;
