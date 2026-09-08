async function run() {
    const r1 = await fetch("http://localhost:8000/api/meetings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: "weekly", meeting_date: "2026-09-08" })
    });
    console.log("Create status:", r1.status);
    const data = await r1.json();
    console.log(data);
    const id = data.id;

    const vttStr = `WEBVTT

00:00:00.000 --> 00:00:08.000
Sarah: Alright team, let me open the incident review for yesterday's database outage. David, can you give a brief timeline?

00:00:09.000 --> 00:00:22.000
David: Sure. At 14:15 UTC, our primary PostgreSQL`;

    const r2 = await fetch(`http://localhost:8000/api/meetings/${id}/transcript/paste`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: vttStr, format: "vtt" })
    });
    console.log("Paste status:", r2.status);
    console.log(await r2.text());
}
run();
