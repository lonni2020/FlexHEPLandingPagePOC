import { useState } from "react";
import {
  ArrowUpRight,
  Check,
  ClipboardCheck,
  FileDown,
  HeartPulse,
  Layers3,
  Mail,
  Sparkles,
  UsersRound,
} from "lucide-react";

const features = [
  {
    number: "01",
    icon: Sparkles,
    title: "Plans that fit the person",
    text: "Shape every exercise around your patient's goals, ability, and day-to-day reality. Adjust reps, frequency, instructions, and more.",
  },
  {
    number: "02",
    icon: UsersRound,
    title: "A shared brain for PTs",
    text: "Find inspiration from your peers, share what works, and keep the clinical conversation moving beyond the treatment room.",
  },
  {
    number: "03",
    icon: FileDown,
    title: "Works wherever your patient is",
    text: "Give your patient a simple digital plan or print a clear, personalized PDF when an app download is not the right fit.",
  },
];

function PlanPreview() {
  return (
    <div className="plan-scene" aria-label="FlexHEP patient plan preview">
      <div className="scene-orbit orbit-one" />
      <div className="scene-orbit orbit-two" />
      <div className="phone-card">
        <div className="phone-topline">
          <span className="tiny-brand"><span className="brand-mark mini">F</span> FlexHEP</span>
          <span className="avatar">JM</span>
        </div>
        <div className="patient-greeting">Good morning, Jamie</div>
        <div className="progress-row">
          <div><span className="progress-label">Your plan</span><strong>65% complete</strong></div>
          <div className="progress-ring">65</div>
        </div>
        <div className="exercise-list">
          <div className="exercise-row active-exercise">
            <div className="exercise-icon teal-icon"><HeartPulse size={18} /></div>
            <div className="exercise-copy"><strong>Seated knee extension</strong><span>3 sets · 12 reps</span></div>
            <Check size={17} className="check" />
          </div>
          <div className="exercise-row">
            <div className="exercise-icon coral-icon"><Layers3 size={18} /></div>
            <div className="exercise-copy"><strong>Wall calf stretch</strong><span>2 sets · 30 sec</span></div>
            <span className="start-pill">Start</span>
          </div>
          <div className="exercise-row muted-exercise">
            <div className="exercise-icon yellow-icon"><ClipboardCheck size={18} /></div>
            <div className="exercise-copy"><strong>Heel raises</strong><span>3 sets · 10 reps</span></div>
          </div>
        </div>
      </div>
      <div className="floating-note note-top"><span className="note-dot" /> Plan updated <strong>just now</strong></div>
      <div className="floating-note note-bottom"><div className="mini-stack"><span /><span /><span /></div><div><strong>Made for you</strong><small>Personalized care</small></div></div>
    </div>
  );
}

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
      <section className="hero-section">
        <nav className="site-nav content-width" aria-label="Main navigation">
          <a className="wordmark" href="/" aria-label="FlexHEP home">
            <span className="brand-mark">F</span>
            <span>Flex<span>HEP</span></span>
          </a>
          <div className="nav-note"><span className="live-dot" /> Built for better follow-through</div>
        </nav>
        <div className="hero-grid content-width">
          <div className="hero-copy">
            <div className="eyebrow"><span className="eyebrow-line" /> The home exercise plan, reimagined</div>
            <h1>Better home care.<br /><em>Stronger outcomes.</em></h1>
            <p className="hero-text">Give your patients a plan that feels made for them, and give yourself a smarter way to build, share, and improve it.</p>
            <div className="hero-proof"><div className="proof-avatars"><span>PT</span><span>JM</span><span>+</span></div><span>Designed with physical therapists<br /><strong>for the people they care for.</strong></span></div>
            <div className="waitlist-wrap">
              {status === "success" ? (
                <div className="success-card" role="status">
                  <div className="success-icon"><Check size={22} /></div>
                  <div><strong>You&apos;re on the list.</strong><span>We&apos;ll let you know when FlexHEP is ready.</span></div>
                </div>
              ) : (
                <form className="waitlist-form" onSubmit={handleSubmit}>
                  <label htmlFor="email">Be first to know when FlexHEP launches</label>
                  <div className="input-row">
                    <div className="email-input"><Mail size={18} /><input id="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@yourpractice.com" required aria-describedby={error ? "form-error" : undefined} /></div>
                    <button type="submit" disabled={status === "loading"}>{status === "loading" ? "Joining..." : "Keep me updated"}<ArrowUpRight size={18} /></button>
                  </div>
                  {error && <p className="form-error" id="form-error" role="alert">{error}</p>}
                  <p className="privacy-note">No noise. Just launch updates from FlexHEP.</p>
                </form>
              )}
            </div>
          </div>
          <div className="hero-visual"><PlanPreview /><div className="visual-caption"><span className="caption-line" /> Your patient's next step, made clear.</div></div>
        </div>
        <div className="scroll-cue"><span>Scroll to see what&apos;s next</span><div className="scroll-line" /></div>
      </section>

      <section className="feature-section">
        <div className="content-width">
          <div className="section-heading"><div><div className="eyebrow dark-eyebrow"><span className="eyebrow-line" /> What you can do with FlexHEP</div><h2>Care that keeps<br /><em>moving forward.</em></h2></div><p>Less friction between your clinical thinking and your patient&apos;s progress. FlexHEP brings it all into one focused space.</p></div>
          <div className="feature-grid">{features.map(({ number, icon: Icon, title, text }) => <article className="feature-card" key={number}><div className="card-top"><span className="feature-number">{number}</span><div className="feature-icon"><Icon size={21} /></div></div><h3>{title}</h3><p>{text}</p><span className="card-arrow"><ArrowUpRight size={16} /></span></article>)}</div>
          <div className="bottom-banner"><div className="banner-mark"><HeartPulse size={20} /></div><div><strong>Built around the way you already practice.</strong><span>Simple for you. Clear for your patients. Better for the journey between visits.</span></div><span className="banner-spark">*</span></div>
        </div>
      </section>
      <footer className="site-footer content-width"><a className="wordmark" href="/" aria-label="FlexHEP home"><span className="brand-mark small-mark">F</span><span>Flex<span>HEP</span></span></a><span>Home exercise, with more humanity.</span><span>© 2026 FlexHEP</span></footer>
    </main>
  );
}

export default App;
