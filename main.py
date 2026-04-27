"""
LASER MICROPHONE - Global Expo Level Animation
================================================
A scientific visualization of a laser microphone system:
Custom-powered laser → Glass reflector (vibrating with sound) →
Photodiode → Amplifier → Sound Card → Laptop

Requirements:
    pip install manim

Run with:
    manim -pqh laser_microphone.py LaserMicrophoneExpo
    
For loop-ready output (no fade-out at end):
    manim -pqh laser_microphone.py LaserMicrophoneExpo
"""

from manim import *
import numpy as np


# ─────────────────────────── COLOUR PALETTE ───────────────────────────
BG          = "#020818"
LASER_COL   = "#7ED80F"
REFLECT_COL = "#D3472F"
GLASS_COL   = "#A8D8EA"
BEAM_GLOW   = "#70CA2C"
SOUND_COL   = "#00FFCC"
PHOTO_COL   = "#FFD700"
AMP_COL     = "#AA44FF"
CARD_COL    = "#33CCFF"
LAPTOP_COL  = "#E0E0E0"
ACCENT      = "#FFFFFF"
DIM         = "#445566"
TITLE_COL   = "#FFFFFF"
SUB_COL     = "#88BBDD"
VOLT_COL    = "#FFAA00"


# ─────────────────────────── HELPERS ──────────────────────────────────
def glow_line(start, end, color=LASER_COL, width=4, layers=4):
    """Return a VGroup of stacked lines simulating a glow effect."""
    g = VGroup()
    for i in range(layers, 0, -1):
        l = Line(start, end,
                 stroke_color=color,
                 stroke_width=width * i * 0.55,
                 stroke_opacity=0.08 + 0.22 * (1 / i))
        g.add(l)
    core = Line(start, end, stroke_color=WHITE,
                stroke_width=width * 0.45, stroke_opacity=0.9)
    g.add(core)
    return g


def sine_wave_points(x_start, x_end, y_center, amplitude, frequency,
                     phase=0, n=300):
    xs = np.linspace(x_start, x_end, n)
    ys = y_center + amplitude * np.sin(frequency * xs + phase)
    return [np.array([x, y, 0]) for x, y in zip(xs, ys)]


def make_wave_mob(x_start, x_end, y_center, amplitude, frequency,
                  phase=0, color=SOUND_COL, width=2):
    pts = sine_wave_points(x_start, x_end, y_center,
                           amplitude, frequency, phase)
    path = VMobject()
    path.set_points_smoothly(pts)
    path.set_stroke(color=color, width=width)
    return path


# ══════════════════════════════════════════════════════════════════════
class LaserMicrophoneExpo(Scene):
    """Full expo-ready looping animation."""

    # ── scene constants ──────────────────────────────────────────────
    LASER_X   = -6.0
    GLASS_X   =  0.2
    PHOTO_X   =  3.8
    AMP_X     =  5.2
    CARD_X    =  6.2
    LAPTOP_X  =  6.2
    Y_BEAM    =  0.0

    def construct(self):
        self.camera.background_color = BG
        self._scene_01_title()
        self._scene_02_system_overview()
        self._scene_03_power_supply()
        self._scene_04_laser_emission()
        self._scene_05_glass_vibration()
        self._scene_06_frequency_modulation()
        self._scene_07_photodiode()
        self._scene_08_amplifier_soundcard()
        self._scene_09_full_loop()

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 01 – CINEMATIC TITLE
    # ══════════════════════════════════════════════════════════════════
    def _scene_01_title(self):
        # Background grid
        grid = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-5, 5, 1],
            background_line_style={"stroke_color": "#0a1a2a",
                                   "stroke_width": 1,
                                   "stroke_opacity": 0.6},
            axis_config={"stroke_opacity": 0},
        ).scale(1)

        # Scanning line sweep
        scan = Line([-8, -5, 0], [-8, 5, 0],
                    stroke_color="#00FFCC", stroke_width=1.5,
                    stroke_opacity=0.5)

        title = Text("LASER MICROPHONE",
                     font="Courier New", font_size=52,
                     color=TITLE_COL, weight=BOLD)
        title.set_stroke(color=LASER_COL, width=1)

        subtitle = Text("Optical Acoustic Detection System",
                        font="Courier New", font_size=20,
                        color=SUB_COL)
        subtitle.next_to(title, DOWN, buff=0.35)

        tagline = Text(
            "Custom Power  ·  Laser Beam  ·  Frequency Modulation  ·  Photodiode  ·  Audio Recovery",
            font="Courier New", font_size=11, color=DIM)
        tagline.next_to(subtitle, DOWN, buff=0.25)

        divider = Line([-4, 0, 0], [4, 0, 0],
                       stroke_color=LASER_COL, stroke_width=1.5)
        divider.next_to(tagline, DOWN, buff=0.3)

        badge = Text("[ INNOTEK TEAM JIGSAW EXPO PROJECT ]",
                     font="Courier New", font_size=13, color=LASER_COL)
        badge.next_to(divider, DOWN, buff=0.2)

        title_group = VGroup(title, subtitle, tagline, divider, badge)
        title_group.center()

        # Laser beam dashes flying in from left
        beams = VGroup(*[
            Line([-8, np.random.uniform(-3, 3), 0],
                 [-6, np.random.uniform(-3, 3), 0],
                 stroke_color=LASER_COL,
                 stroke_width=np.random.uniform(0.5, 2),
                 stroke_opacity=np.random.uniform(0.2, 0.7))
            for _ in range(12)
        ])

        self.play(FadeIn(grid, run_time=0.4))
        self.play(
            scan.animate.move_to([8, 0, 0]),
            rate_func=linear, run_time=0.9
        )
        self.remove(scan)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=RIGHT * 0.4) for b in beams],
                lag_ratio=0.07
            ),
            run_time=0.6
        )
        self.play(
            Write(title, run_time=1.4),
            FadeOut(beams, run_time=0.8),
        )
        self.play(
            FadeIn(subtitle, shift=UP * 0.15, run_time=0.7),
            FadeIn(tagline,  shift=UP * 0.1,  run_time=0.8),
        )
        self.play(
            GrowFromCenter(divider, run_time=0.5),
            FadeIn(badge, run_time=0.5),
        )
        self.wait(1.8)
        self.play(FadeOut(VGroup(grid, title_group), run_time=0.7))

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 02 – FULL SYSTEM DIAGRAM (birds-eye schematic)
    # ══════════════════════════════════════════════════════════════════
    def _scene_02_system_overview(self):
        header = Text("SYSTEM OVERVIEW",
                      font="Courier New", font_size=18,
                      color=ACCENT).to_edge(UP, buff=0.18)
        underline = Line(header.get_left(), header.get_right(),
                         stroke_color=LASER_COL, stroke_width=1.5)
        underline.next_to(header, DOWN, buff=0.05)

        # ── component blocks ─────────────────────────────────────────
        def comp_box(label, sublabel, col, width=1.05, height=0.75):
            rect = RoundedRectangle(corner_radius=0.08,
                                    width=width, height=height,
                                    fill_color=col, fill_opacity=0.15,
                                    stroke_color=col, stroke_width=2)
            t1 = Text(label, font="Courier New",
                      font_size=9, color=col, weight=BOLD)
            t2 = Text(sublabel, font="Courier New",
                      font_size=7, color=col)
            t2.set_opacity(0.75)
            t1.move_to(rect.get_center() + UP * 0.17)
            t2.move_to(rect.get_center() + DOWN * 0.17)
            return VGroup(rect, t1, t2)

        psu   = comp_box("PSU",        "3 V Regulated",  VOLT_COL)
        laser = comp_box("LASER",      "600 nm / 5mW",   LASER_COL)
        glass = comp_box("GLASS",      "Reflector",      GLASS_COL, 1.1)
        photo = comp_box("PHOTODIODE", "OPT-101",        PHOTO_COL, 1.45)
        amp   = comp_box("AMPLIFIER",  "LM386 x20",      AMP_COL,   1.35)
        card  = comp_box("SOUND CARD", "USB / 44.1 kHz", CARD_COL,  1.45)
        laptop= comp_box("LAPTOP",     "Audacity",       LAPTOP_COL,1.35)

        comps = VGroup(psu, laser, glass, photo, amp, card, laptop)
        comps.arrange(RIGHT, buff=0.65)
        comps.center().shift(DOWN * 0.1)
        comps.scale(0.82)

        # Connecting arrows
        def flow_arrow(a, b, col=DIM):
            start = a.get_right() + RIGHT * 0.02
            end   = b.get_left()  + LEFT  * 0.02
            return Arrow(start, end,
                         buff=0, stroke_color=col,
                         stroke_width=1.8, max_tip_length_to_length_ratio=0.2,
                         color=col)

        arrows = VGroup(
            flow_arrow(psu,    laser,  VOLT_COL),
            flow_arrow(laser,  glass,  LASER_COL),
            flow_arrow(glass,  photo,  REFLECT_COL),
            flow_arrow(photo,  amp,    PHOTO_COL),
            flow_arrow(amp,    card,   AMP_COL),
            flow_arrow(card,   laptop, CARD_COL),
        )

        # Signal type labels above arrows
        sig_labels = [
            ("DC Power",    VOLT_COL),
            ("Laser\nBeam",  LASER_COL),
            ("Modulated\nReflection", REFLECT_COL),
            ("Analog\nVoltage", PHOTO_COL),
            ("Boosted\nSignal", AMP_COL),
            ("Digital\nAudio", CARD_COL),
        ]
        arrow_tags = VGroup()
        for arrow, (txt, col) in zip(arrows, sig_labels):
            t = Text(txt, font="Courier New", font_size=8,
                color=col, line_spacing=0.85)
            t.move_to(arrow.get_center() + UP * 0.5)
            arrow_tags.add(t)

        self.play(FadeIn(header), GrowFromCenter(underline), run_time=0.5)
        self.play(
            LaggedStart(
                *[FadeIn(c, scale=0.85) for c in comps],
                lag_ratio=0.12
            ), run_time=1.2
        )
        self.play(
            LaggedStart(
                *[GrowArrow(a) for a in arrows],
                lag_ratio=0.1
            ), run_time=1.0
        )
        self.play(
            LaggedStart(
                *[FadeIn(t, shift=UP * 0.06) for t in arrow_tags],
                lag_ratio=0.08
            ), run_time=0.8
        )
        self.wait(2.0)
        self.play(
            FadeOut(VGroup(header, underline, comps, arrows, arrow_tags)),
            run_time=0.6
        )

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 03 – CUSTOM POWER SUPPLY
    # ══════════════════════════════════════════════════════════════════
    def _scene_03_power_supply(self):
        title = self._section_title("STEP 1 — CUSTOM POWER SUPPLY")

        # Battery icon (old, crossed out)
        batt = Rectangle(width=1.0, height=0.55,
                          fill_color="#333", fill_opacity=0.9,
                          stroke_color=DIM, stroke_width=2)
        batt_cap = Rectangle(width=0.12, height=0.3,
                              fill_color=DIM, fill_opacity=1,
                              stroke_color=DIM)
        batt_cap.next_to(batt, RIGHT, buff=0)
        batt_lbl = Text("2×AAA\n1.5V", font="Courier New",
                        font_size=9, color=DIM)
        batt_lbl.move_to(batt)
        batt_group = VGroup(batt, batt_cap, batt_lbl)
        batt_group.shift(LEFT * 3.5 + UP * 0.5)

        cross = Cross(batt_group, stroke_color=RED, stroke_width=4)

        # PSU block
        psu_rect = RoundedRectangle(corner_radius=0.12,
                                    width=2.0, height=1.1,
                                    fill_color=VOLT_COL, fill_opacity=0.15,
                                    stroke_color=VOLT_COL, stroke_width=2.5)
        psu_lbl  = Text("REGULATED PSU", font="Courier New",
                        font_size=12, color=VOLT_COL, weight=BOLD)
        psu_v    = Text("3V DC · ±0.01V stability",
                font="Courier New", font_size=8, color=VOLT_COL)
        psu_lbl.move_to(psu_rect.get_center() + UP * 0.2)
        psu_v.move_to(psu_rect.get_center() + DOWN * 0.2)
        psu_group = VGroup(psu_rect, psu_lbl, psu_v)
        psu_group.shift(RIGHT * 1.5 + UP * 0.5)

        arrow_psu = Arrow(
            psu_group.get_right() + RIGHT * 0.1,
            psu_group.get_right() + RIGHT * 2.2,
            color=VOLT_COL, stroke_width=3,
            max_tip_length_to_length_ratio=0.15
        )
        laser_stub = Text("→ TO LASER",
                          font="Courier New", font_size=11,
                          color=LASER_COL)
        laser_stub.next_to(arrow_psu, RIGHT, buff=0.1)

        # Why stable power matters
        bullets = VGroup(
            *[Text(t, font="Courier New", font_size=11, color=ACCENT)
              for t in [
                  "✦  Fluctuating voltage  →  noisy beam intensity",
                  "✦  Regulated PSU  →  constant photon flux",
                  "✦  Eliminates amplitude noise before it starts",
              ]]
        )
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        bullets.shift(DOWN * 1.6 + LEFT * 0.5)

        # Voltage stability graph
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 2, 0.5],
                  x_length=3.2, y_length=1.4,
                  axis_config={"color": DIM, "stroke_width": 1.5})
        ax.shift(RIGHT * 3.8 + DOWN * 1.7)

        noisy = ax.plot(
            lambda x: 1.5 + 0.35 * np.sin(18 * x) + 0.2 * np.sin(40 * x),
            x_range=[0, 2.4], color=RED, stroke_width=1.8)
        stable = ax.plot(
            lambda x: 1.5,
            x_range=[2.6, 5], color=VOLT_COL, stroke_width=2.5)
        divider_v = DashedLine(
            ax.c2p(2.5, 0), ax.c2p(2.5, 2),
            dash_length=0.08, color=DIM, stroke_width=1)
        noisy_lbl  = Text("Battery", font="Courier New",
                          font_size=8, color=RED).next_to(ax.c2p(1.2, 1.9), UP, buff=0.05)
        stable_lbl = Text("PSU", font="Courier New",
                          font_size=8, color=VOLT_COL).next_to(ax.c2p(3.8, 1.9), UP, buff=0.05)

        graph_grp = VGroup(ax, noisy, stable, divider_v, noisy_lbl, stable_lbl)

        self.play(FadeIn(title), run_time=0.4)
        self.play(FadeIn(batt_group), run_time=0.5)
        self.play(GrowFromCenter(cross), run_time=0.4)
        self.play(FadeIn(psu_group, scale=0.9), run_time=0.6)
        self.play(GrowArrow(arrow_psu), FadeIn(laser_stub), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bullets],
                        lag_ratio=0.2),
            run_time=0.8
        )
        self.play(FadeIn(graph_grp), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(VGroup(title, batt_group, cross, psu_group,
                                 arrow_psu, laser_stub, bullets,
                                 graph_grp)), run_time=0.6)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 04 – LASER EMISSION & BEAM PATH
    # ══════════════════════════════════════════════════════════════════
    def _scene_04_laser_emission(self):
        title = self._section_title("STEP 2 — LASER EMISSION")

        # Laser housing
        housing = Rectangle(width=1.4, height=0.5,
                             fill_color="#1a1a2e", fill_opacity=0.95,
                             stroke_color=LASER_COL, stroke_width=2.5)
        housing.shift(LEFT * 5.2)
        housing_lbl = Text("600 nm LASER", font="Courier New",
                           font_size=9, color=LASER_COL)
        housing_lbl.next_to(housing, DOWN, buff=0.1)
        aperture = Dot(housing.get_right(), color=LASER_COL, radius=0.08)

        # Beam with glow
        beam_end = np.array([self.GLASS_X - 0.25, self.Y_BEAM, 0])
        beam_start = housing.get_right()
        beam = glow_line(beam_start, beam_end, LASER_COL, width=5)

        # Photon wave annotation
        photon_label = MathTex(
            r"\lambda = 600\,\text{nm}",
            font_size=22, color=LASER_COL
        ).next_to(beam_end + LEFT * 1.5, UP, buff=0.35)

        coherent_label = Text("Coherent · Monochromatic · Collimated",
                              font="Courier New", font_size=10, color=DIM)
        coherent_label.next_to(photon_label, DOWN, buff=0.12)

        # Power spec card
        spec = self._spec_card(
            "LASER SPEC",
            [("Wavelength", "600 nm (red)"),
             ("Power",      "≤5 mW (Class IIIA)"),
             ("Supply",     "3 V regulated"),
             ("Beam ⌀",    "~3 mm collimated")],
            color=LASER_COL
        )
        spec.shift(RIGHT * 3.2 + DOWN * 1.2)

        self.play(FadeIn(title), run_time=0.4)
        self.play(FadeIn(housing), FadeIn(housing_lbl), run_time=0.5)
        self.play(GrowFromPoint(aperture, housing.get_right()), run_time=0.3)

        # Animate beam growing
        self.play(
            Create(beam, run_time=0.8, rate_func=linear),
        )
        self.play(
            FadeIn(photon_label, shift=UP * 0.1),
            FadeIn(coherent_label),
            run_time=0.5
        )
        self.play(FadeIn(spec, scale=0.9), run_time=0.5)
        self.wait(1.8)
        self.play(
            FadeOut(VGroup(title, housing, housing_lbl, aperture,
                           beam, photon_label, coherent_label, spec)),
            run_time=0.6
        )

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 05 – GLASS VIBRATION
    # ══════════════════════════════════════════════════════════════════
    def _scene_05_glass_vibration(self):
        title = self._section_title("STEP 3 — GLASS VIBRATION")

        # Glass pane
        glass_rect = Rectangle(width=0.18, height=2.8,
                                fill_color=GLASS_COL, fill_opacity=0.22,
                                stroke_color=GLASS_COL, stroke_width=2.2)
        glass_rect.move_to([self.GLASS_X, 0, 0])
        glass_lbl = Text("GLASS\nPANE", font="Courier New",
                         font_size=9, color=GLASS_COL)
        glass_lbl.next_to(glass_rect, UP, buff=0.15)

        # Speaker / sound source inside
        spk_circle = Circle(radius=0.55, fill_color="#0a0a1a",
                             fill_opacity=0.9,
                             stroke_color=SOUND_COL, stroke_width=2)
        spk_circle.shift(LEFT * 1.5)
        spk_icon = Text("♪", font_size=22, color=SOUND_COL)
        spk_icon.move_to(spk_circle)
        spk_lbl = Text("Sound Source", font="Courier New",
                       font_size=9, color=SOUND_COL)
        spk_lbl.next_to(spk_circle, DOWN, buff=0.1)

        # Sound waves expanding from speaker
        def make_arc_wave(r, alpha):
            arc = Arc(radius=r, angle=PI * 0.7,
                      start_angle=-PI * 0.35,
                      stroke_color=SOUND_COL,
                      stroke_width=1.5,
                      stroke_opacity=alpha)
            arc.shift(spk_circle.get_center())
            return arc

        sound_waves = VGroup(
            *[make_arc_wave(0.7 + 0.35 * i, 0.7 - 0.15 * i)
              for i in range(4)]
        )

        # Incident beam
        beam_in = glow_line(
            np.array([self.LASER_X + 0.7, self.Y_BEAM, 0]),
            np.array([self.GLASS_X - 0.09, self.Y_BEAM, 0]),
            LASER_COL, width=4
        )
        in_lbl = Text("Incident Beam  f₀",
                      font="Courier New", font_size=10, color=LASER_COL)
        in_lbl.next_to(beam_in, UP, buff=0.15)

        # Vibration detail – magnified view
        mag_circle = Circle(radius=1.1, fill_color=BG, fill_opacity=0.85,
                             stroke_color=GLASS_COL, stroke_width=1.5)
        mag_circle.shift(RIGHT * 4.5 + DOWN * 0.5)
        mag_title = Text("MICRO-VIBRATION", font="Courier New",
                         font_size=9, color=GLASS_COL)
        mag_title.next_to(mag_circle, UP, buff=0.1)

        # Wavy glass surface in magnified view
        static_glass  = Line([4.4, -0.9, 0], [4.4,  0.5, 0],
                              stroke_color=GLASS_COL, stroke_width=2.5,
                              stroke_opacity=0.4)
        vibrate_glass = make_wave_mob(4.4, 4.4, -0.5,
                                      0.0, 2.0, color=GLASS_COL, width=2.5)

        # Displacement equation
        # disp_eq = MathTex(r"x(t) = A\cos(2\pi f_{s}\,t + \phi)",
        #                   font_size=18, color=GLASS_COL)
        # disp_eq.next_to(mag_circle, DOWN, buff=0.18)

        self.play(FadeIn(title), run_time=0.4)
        self.play(FadeIn(glass_rect), FadeIn(glass_lbl), run_time=0.5)
        self.play(FadeIn(spk_circle), FadeIn(spk_icon),
                  FadeIn(spk_lbl), run_time=0.5)
        self.play(
            LaggedStart(
                *[Create(w) for w in sound_waves],
                lag_ratio=0.15
            ), run_time=0.8
        )
        self.play(Create(beam_in, run_time=0.6), FadeIn(in_lbl), run_time=0.5)

        # Animate glass vibration (wiggle)
        self.play(
            glass_rect.animate(rate_func=there_and_back, run_time=0.35)
                      .shift(RIGHT * 0.06),
        )
        for _ in range(4):
            self.play(
                glass_rect.animate(rate_func=there_and_back, run_time=0.22)
                          .shift(RIGHT * 0.06),
            )

        self.play(
            FadeIn(mag_circle), FadeIn(mag_title),
            FadeIn(static_glass), run_time=0.5
        )
    
        self.play(
            FadeOut(VGroup(title, glass_rect, glass_lbl, spk_circle,
                           spk_icon, spk_lbl, sound_waves, beam_in,
                           in_lbl, mag_circle, mag_title, static_glass,
                           vibrate_glass)),
            run_time=0.6
        )

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 06 – DOPPLER / PHASE MODULATION
    # ══════════════════════════════════════════════════════════════════
    def _scene_06_frequency_modulation(self):
        title = self._section_title("STEP 4 — INTENSITY MODULATION")

        subtitle = Text(
            "Glass vibration changes reflected beam brightness — photodiode reads intensity",
            font="Courier New", font_size=11, color=SUB_COL
        ).next_to(title, DOWN, buff=0.08)

        # Axes for frequency-vs-time
        ax = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-1.6, 1.6, 0.5],
            x_length=7.5, y_length=3.2,
            axis_config={"color": DIM, "stroke_width": 1.5,
                         "include_tip": True},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).shift(DOWN * 0.6)

        x_lbl = Text("Time →", font="Courier New",
                     font_size=10, color=DIM)
        x_lbl.next_to(ax.x_axis.get_right(), RIGHT, buff=0.1)
        y_lbl = Text("Displacement / Frequency", font="Courier New",
                     font_size=9, color=DIM)
        y_lbl.next_to(ax.y_axis.get_top(), UP, buff=0.1)

        # Sound signal (audio frequency ~1 kHz modelled slow for vis)
        sound_curve = ax.plot(
            lambda x: 1.1 * np.sin(x),
            x_range=[0, 4*PI], color=SOUND_COL, stroke_width=2.5
        )
        sound_lbl = Text("Audio Signal  fₛ",
                         font="Courier New", font_size=10, color=SOUND_COL)
        sound_lbl.next_to(ax.c2p(0.4, 1.1), LEFT * 0.25, buff=0.1)

        # Incident beam (constant high-frequency carrier — shown as uniform sine)
        incident_curve = ax.plot(
            lambda x: 0.55 * np.sin(8 * x),
            x_range=[0, 4*PI], color=LASER_COL, stroke_width=1.8
        )
        incident_lbl = Text("Incident  f₀",
                            font="Courier New", font_size=10, color=LASER_COL)
        incident_lbl.next_to(ax.c2p(PI * 0.5, 0.55), UP, buff=0.1)
        incident_lbl.shift(UP * 0.2 + RIGHT * 2)

        # Reflected beam (frequency modulated)
        def fm_signal(x):
            mod = np.sin(x)
            return 0.55 * np.sin(8 * x + 2.5 * np.sin(x))

        reflected_curve = ax.plot(
            fm_signal,
            x_range=[0, 4*PI], color=REFLECT_COL, stroke_width=2.2
        )
        reflected_lbl = Text("Reflected  — Intensity Modulated",
                             font="Courier New", font_size=10,
                             color=REFLECT_COL)
        reflected_lbl.next_to(ax.c2p(PI * 2, -0.9), DOWN, buff=0.12)
        reflected_lbl.shift(RIGHT * 1)

        # Doppler equation
       

        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.5)
        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)
        self.play(Create(sound_curve), FadeIn(sound_lbl), run_time=0.8)
        self.play(Create(incident_curve), FadeIn(incident_lbl), run_time=0.7)
        self.play(Create(reflected_curve), FadeIn(reflected_lbl), run_time=0.9)
        self.wait(2.0)
        self.play(
            FadeOut(VGroup(title, subtitle, ax, x_lbl, y_lbl,
                           sound_curve, sound_lbl,
                           incident_curve, incident_lbl,
                           reflected_curve, reflected_lbl,
                           q)),
            run_time=0.6
        )

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 07 – PHOTODIODE DETECTION
    # ══════════════════════════════════════════════════════════════════
    def _scene_07_photodiode(self):
        title = self._section_title("STEP 5 — PHOTODIODE DETECTION")

        # Reflected beam coming in from glass
        r_beam = glow_line(
            np.array([self.GLASS_X + 0.15, 0.15, 0]),
            np.array([self.PHOTO_X - 0.55, 0.15, 0]),
            REFLECT_COL, width=4
        )

        # Photodiode symbol
        pd_tri = Triangle(fill_color=PHOTO_COL, fill_opacity=0.7,
                          stroke_color=PHOTO_COL, stroke_width=2)
        pd_tri.scale(0.3).rotate(-PI / 2)
        pd_line = Line(pd_tri.get_right() + RIGHT * 0.01,
                       pd_tri.get_right() + RIGHT * 0.3,
                       stroke_color=PHOTO_COL, stroke_width=2.5)
        pd_body = VGroup(pd_tri, pd_line)
        pd_body.shift(np.array([self.PHOTO_X, 0.15, 0]))

        pd_box = RoundedRectangle(corner_radius=0.1, width=1.4, height=0.85,
                                  fill_color="#100820", fill_opacity=0.9,
                                  stroke_color=PHOTO_COL, stroke_width=2)
        pd_box.move_to(pd_body)
        pd_lbl = Text("PHOTODIODE", font="Courier New",
                      font_size=9, color=PHOTO_COL, weight=BOLD)
        pd_sub = Text("OPT-101  I→V", font="Courier New",
                      font_size=8, color=PHOTO_COL)
        pd_lbl.move_to(pd_box.get_center() + UP * 0.2)
        pd_sub.move_to(pd_box.get_center() + DOWN * 0.2)
        pd_group = VGroup(pd_box, pd_lbl, pd_sub)
        pd_group.move_to(np.array([self.PHOTO_X, 0.15, 0]))

        # How it works panel
        explain = VGroup(
            *[Text(t, font="Courier New", font_size=10, color=ACCENT)
              for t in [
                  "1. Reflected beam hits active area",
                  "2. Photons → electron-hole pairs",
                  "3. Photocurrent ∝ beam intensity",
                  "4. I→V converter outputs voltage",
              ]]
        )
        explain.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explain.shift(LEFT * 1.8 + DOWN * 1.9)

        # Output voltage wave
        ax2 = Axes(x_range=[0, 2*PI, PI], y_range=[-1.2, 1.2, 0.5],
                   x_length=3.2, y_length=1.4,
                   axis_config={"color": DIM, "stroke_width": 1.2})
        ax2.shift(RIGHT * 3.8 + DOWN * 1.9)
        v_wave = ax2.plot(
            lambda x: 0.9 * np.sin(x + 0.3) + 0.15 * np.sin(3.1 * x),
            x_range=[0, 2*PI], color=PHOTO_COL, stroke_width=2.2
        )
        ax2_lbl = Text("V_out (raw audio)", font="Courier New",
                       font_size=8, color=PHOTO_COL)
        ax2_lbl.next_to(ax2, DOWN, buff=0.05)

        # Equation
        eq = MathTex(r"V_{out} = R_f \cdot I_{ph}",
                     font_size=20, color=PHOTO_COL)
        eq.next_to(pd_group, UP, buff=0.5)

        self.play(FadeIn(title), run_time=0.4)
        self.play(Create(r_beam, run_time=0.6))
        self.play(FadeIn(pd_group, scale=0.85), run_time=0.5)
        self.play(Write(eq), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(e, shift=RIGHT * 0.08) for e in explain],
                        lag_ratio=0.18),
            run_time=0.9
        )
        self.play(Create(ax2), Create(v_wave), FadeIn(ax2_lbl), run_time=0.7)
        self.wait(2.0)
        self.play(
            FadeOut(VGroup(title, r_beam, pd_group, eq, explain,
                           ax2, v_wave, ax2_lbl)),
            run_time=0.6
        )

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 08 – AMPLIFIER & SOUND CARD
    # ══════════════════════════════════════════════════════════════════
    def _scene_08_amplifier_soundcard(self):
        title = self._section_title("STEP 6 — AMPLIFICATION & DIGITISATION")

        # Signal path: PD → Amp → Sound Card → Laptop
        def comp(label, sublabel, col, pos):
            rect = RoundedRectangle(corner_radius=0.1, width=1.6, height=0.9,
                                    fill_color=col, fill_opacity=0.12,
                                    stroke_color=col, stroke_width=2)
            t1 = Text(label,    font="Courier New", font_size=11,
                      color=col, weight=BOLD)
            t2 = Text(sublabel, font="Courier New", font_size=8,  color=col)
            t1.move_to(rect.get_center() + UP * 0.18)
            t2.move_to(rect.get_center() + DOWN * 0.18)
            g = VGroup(rect, t1, t2)
            g.shift(pos)
            return g

        pd_box   = comp("PHOTODIODE", "~mV signal",
                        PHOTO_COL, LEFT * 5.0 + UP * 0.2)
        amp_box  = comp("LM386 AMP", "Gain = 20×",
                        AMP_COL,   LEFT * 1.8 + UP * 0.2)
        card_box = comp("SOUND CARD", "USB 44.1kHz",
                        CARD_COL,  RIGHT * 1.8 + UP * 0.2)
        lap_box  = comp("LAPTOP",    "Audacity / DAW",
                        LAPTOP_COL, RIGHT * 5.0 + UP * 0.2)

        def arr(a, b, col):
            return Arrow(a.get_right() + RIGHT * 0.05,
                         b.get_left()  + LEFT  * 0.05,
                         color=col, buff=0, stroke_width=2,
                         max_tip_length_to_length_ratio=0.18)

        a1 = arr(pd_box, amp_box, PHOTO_COL)
        a2 = arr(amp_box, card_box, AMP_COL)
        a3 = arr(card_box, lap_box, CARD_COL)

        # Before and after amp signals
        ax_s = Axes(x_range=[0, 2*PI, 1], y_range=[-1.6, 1.6, 0.5],
                    x_length=2.5, y_length=1.3,
                    axis_config={"color": DIM, "stroke_width": 1})
        ax_s.shift(LEFT * 1.8 + DOWN * 2.0)
        before = ax_s.plot(
            lambda x: 0.12 * np.sin(x), x_range=[0, 2*PI],
            color=PHOTO_COL, stroke_width=2)
        after = ax_s.plot(
            lambda x: 1.1 * np.sin(x), x_range=[0, 2*PI],
            color=AMP_COL, stroke_width=2)
        before_lbl = Text("Before amp (mV)",
                          font="Courier New", font_size=8, color=PHOTO_COL)
        after_lbl  = Text("After amp  (×20)",
                          font="Courier New", font_size=8, color=AMP_COL)
        before_lbl.next_to(ax_s, DOWN, buff=0.06)
        after_lbl.next_to(before_lbl, DOWN, buff=0.06)

        # Digitisation / ADC illustration
        ax_d = Axes(x_range=[0, 2*PI, 1], y_range=[-1.4, 1.4, 0.5],
                    x_length=2.5, y_length=1.3,
                    axis_config={"color": DIM, "stroke_width": 1})
        ax_d.shift(RIGHT * 1.8 + DOWN * 2.0)

        # Staircase (quantised) signal
        stair_pts = []
        for i in range(32):
            x = i * (2*PI/32)
            y = round(np.sin(x) * 6) / 6
            if i > 0:
                stair_pts.append(ax_d.c2p(x, stair_pts[-1][1]))
            stair_pts.append(ax_d.c2p(x, y))

        stair = VMobject(stroke_color=CARD_COL, stroke_width=2)
        stair.set_points_as_corners(stair_pts)

        adc_lbl = Text("",
                       font="Courier New", font_size=8, color=CARD_COL)
        adc_lbl.next_to(ax_d, DOWN, buff=0.06)
        aux_note = Text("3.5 mm AUX  →  USB Sound Card  →  Laptop",
                        font="Courier New", font_size=10, color=ACCENT)
        aux_note.shift(DOWN * 3.3)

        self.play(FadeIn(title), run_time=0.4)
        self.play(
            LaggedStart(
                FadeIn(pd_box), FadeIn(amp_box),
                FadeIn(card_box), FadeIn(lap_box),
                lag_ratio=0.15
            ), run_time=1.0
        )
        self.play(
            LaggedStart(
                GrowArrow(a1), GrowArrow(a2), GrowArrow(a3),
                lag_ratio=0.15
            ), run_time=0.7
        )
        self.play(
            Create(ax_s), Create(before), Create(after),
            FadeIn(before_lbl), FadeIn(after_lbl), run_time=0.8
        )
        self.play(
            Create(ax_d), Create(stair),
            FadeIn(adc_lbl), run_time=0.7
        )
        self.play(FadeIn(aux_note, shift=UP * 0.08), run_time=0.4)
        self.wait(2.0)
        self.play(
            FadeOut(VGroup(title, pd_box, amp_box, card_box, lap_box,
                           a1, a2, a3, ax_s, before, after,
                           before_lbl, after_lbl,
                           ax_d, stair, adc_lbl, aux_note)),
            run_time=0.6
        )

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 09 – FULL ANIMATED SYSTEM LOOP
    # ══════════════════════════════════════════════════════════════════
    def _scene_09_full_loop(self):
        title = self._section_title("COMPLETE SYSTEM — LIVE OPERATION")

        # ── static layout ─────────────────────────────────────────────
        Y = 0.35

        # PSU
        psu_rect = self._mini_box("PSU", "3 V", VOLT_COL,
                                  [-6.0, Y + 0.0, 0], 0.9, 0.55)
        # Laser
        laser_rect = self._mini_box("LASER", "600nm", LASER_COL,
                                    [-4.4, Y, 0], 0.95, 0.55)
        # Glass
        glass_rect = Rectangle(width=0.14, height=2.0,
                                fill_color=GLASS_COL, fill_opacity=0.2,
                                stroke_color=GLASS_COL, stroke_width=2)
        glass_rect.move_to([self.GLASS_X, Y, 0])
        glass_lbl = Text("GLASS", font="Courier New",
                         font_size=7, color=GLASS_COL)
        glass_lbl.next_to(glass_rect, UP, buff=0.08)

        # Speaker
        spk = Circle(radius=0.35, fill_color="#0a0a1a", fill_opacity=0.9,
                     stroke_color=SOUND_COL, stroke_width=1.8)
        spk.move_to([-1.5, Y, 0])
        spk_icon = Text("♪", font_size=16, color=SOUND_COL).move_to(spk)

        # Photodiode
        pd_rect = self._mini_box("PD", "OPT101", PHOTO_COL,
                                 [2.5, Y, 0], 0.95, 0.55)
        # Amplifier
        amp_rect = self._mini_box("AMP", "LM386", AMP_COL,
                                  [4.1, Y, 0], 0.85, 0.55)
        # Sound card
        sc_rect = self._mini_box("SC", "USB", CARD_COL,
                                 [5.4, Y, 0], 0.75, 0.55)
        # Laptop
        lap_rect = self._mini_box("💻", "Laptop", LAPTOP_COL,
                                  [6.5, Y, 0], 0.75, 0.55)

        static = VGroup(psu_rect, laser_rect, glass_rect, glass_lbl,
                        spk, spk_icon, pd_rect, amp_rect, sc_rect, lap_rect)

        # Power wire
        pw_arrow = Arrow(psu_rect.get_right(), laser_rect.get_left(),
                         buff=0.04, color=VOLT_COL, stroke_width=2.5,
                         max_tip_length_to_length_ratio=0.2)

        # ── draw scene ────────────────────────────────────────────────
        self.play(FadeIn(title), run_time=0.4)
        self.play(FadeIn(static), GrowArrow(pw_arrow), run_time=0.8)

        # ── animated laser beam (travels from laser to glass) ─────────
        beam_in_pts = [
            np.array([-3.92, Y, 0]),
            np.array([self.GLASS_X - 0.07, Y, 0])
        ]
        beam_refl_pts = [
            np.array([self.GLASS_X + 0.07, Y + 0.05, 0]),
            np.array([2.02, Y + 0.05, 0])
        ]

        beam_in   = glow_line(*beam_in_pts,   LASER_COL,   width=4)
        beam_refl = glow_line(*beam_refl_pts, REFLECT_COL, width=3)

        # Downstream arrows
        def mini_arrow(x1, x2, y, col):
            return Arrow([x1, y, 0], [x2, y, 0],
                         buff=0.04, color=col, stroke_width=2,
                         max_tip_length_to_length_ratio=0.22)

        arr_pd_amp = mini_arrow(2.98, 3.67, Y, PHOTO_COL)
        arr_amp_sc = mini_arrow(4.52, 5.02, Y, AMP_COL)
        arr_sc_lap = mini_arrow(5.77, 6.12, Y, CARD_COL)

        self.play(
            Create(beam_in, rate_func=linear, run_time=0.55),
        )
        self.play(
            Create(beam_refl, rate_func=linear, run_time=0.45),
            GrowArrow(arr_pd_amp),
        )
        self.play(
            GrowArrow(arr_amp_sc), GrowArrow(arr_sc_lap), run_time=0.5
        )

        # ── glass vibration animation ─────────────────────────────────
        def vibrate():
            return [
                glass_rect.animate(rate_func=there_and_back,
                                   run_time=0.18).shift(RIGHT * 0.05)
                for _ in range(3)
            ]

        # ── sound wave pulses ─────────────────────────────────────────
        wave_arcs = VGroup(*[
            Arc(radius=0.45 + 0.28 * i,
                angle=PI * 0.65,
                start_angle=-PI * 0.32,
                stroke_color=SOUND_COL,
                stroke_width=1.5,
                stroke_opacity=0.7 - 0.15 * i)
            .shift(spk.get_center())
            for i in range(3)
        ])

        # ── waveform display on laptop ─────────────────────────────────
        ax_lap = Axes(x_range=[0, 2*PI, 1], y_range=[-1, 1, 0.5],
                      x_length=1.5, y_length=0.7,
                      axis_config={"color": DIM, "stroke_width": 0.8})
        ax_lap.next_to(lap_rect, DOWN, buff=0.25)

        wave_display = ax_lap.plot(
            lambda x: 0.7 * np.sin(x) + 0.2 * np.sin(3 * x),
            x_range=[0, 2*PI], color=CARD_COL, stroke_width=1.8
        )
        lap_wave_lbl = Text("Recovered Audio",
                            font="Courier New", font_size=7, color=CARD_COL)
        lap_wave_lbl.next_to(ax_lap, DOWN, buff=0.06)

        # ── step labels beneath everything ───────────────────────────
        step_labels = [
            (psu_rect,   "Stable\nPower",    VOLT_COL),
            (laser_rect, "Laser\nEmission",  LASER_COL),
            (glass_rect, "Vibrating\nGlass", GLASS_COL),
            (pd_rect,    "Photodiode\nDetection", PHOTO_COL),
            (amp_rect,   "Amplify\n×20",    AMP_COL),
            (sc_rect,    "Digitise\nAudio", CARD_COL),
            (lap_rect,   "Display\nResult", LAPTOP_COL),
        ]
        labels_grp = VGroup()
        for mob, txt, col in step_labels:
            lbl = Text(txt, font="Courier New", font_size=9,
                       color=col, line_spacing=0.9)
            lbl.next_to(mob, DOWN, buff=0.45 if mob is glass_rect else 0.32)
            labels_grp.add(lbl)

        self.play(
            LaggedStart(*vibrate(), lag_ratio=0.1),
            Create(wave_arcs, run_time=0.5),
            run_time=0.6
        )
        # self.play(
        #     Create(ax_lap), Create(wave_display),
        #     FadeIn(lap_wave_lbl), run_time=0.7
        # )
        # self.play(
        #     LaggedStart(
        #         *[FadeIn(l, shift=DOWN * 0.06) for l in labels_grp],
        #         lag_ratio=0.1
        #     ), run_time=0.9
        # )

        # ── pulse animation: colour flash along the chain ─────────────
        chain_mobs = [
            laser_rect, beam_in, glass_rect, beam_refl,
            pd_rect, arr_pd_amp, amp_rect, arr_amp_sc,
            sc_rect, arr_sc_lap, lap_rect
        ]
        for mob in chain_mobs:
            self.play(
                mob.animate(rate_func=there_and_back, run_time=0.12)
                   .set_stroke(WHITE, width=6),
            )

        self.wait(0.5)

        # ── principle summary overlay ─────────────────────────────────
        summary_bg = Rectangle(
            width=13.0, height=2.6,
            fill_color="#010C18", fill_opacity=0.92,
            stroke_color=ACCENT, stroke_width=3
        ).shift(DOWN * 3.2)

        line1 = Text(
            "Sound vibrates glass  →  Glass modulates laser  →  Photodiode converts light to voltage",
            font="Courier New", font_size=11, color=ACCENT,
            t2c={"Sound vibrates glass": SOUND_COL,
                "modulates laser": LASER_COL,
                "Photodiode": PHOTO_COL}
)
        line2 = Text(
            "Amp boosts signal  →  Sound card digitises  →  Audio recovered on laptop",
            font="Courier New", font_size=11, color=ACCENT,
            t2c={"Amp boosts": AMP_COL,
                "Sound card": CARD_COL,
                "Audio recovered": CARD_COL}
)

        line1.move_to(summary_bg.get_center() + UP * 0.55)
        line2.move_to(summary_bg.get_center() + DOWN * 0.55)

        self.play(FadeIn(summary_bg), FadeIn(line1), FadeIn(line2), run_time=0.6)
        self.wait(2.5)

        # ── loop tag ─────────────────────────────────────────────────
        # loop_tag = Text("[ LOOPING ]", font="Courier New",
        #                 font_size=11, color=LASER_COL)
        # loop_tag.to_corner(DR, buff=0.2)
        # self.play(FadeIn(loop_tag), run_time=0.3)
        # self.wait(1.0)

        # ── DO NOT FADE OUT — hold last frame for seamless loop ────────
        # Animation ends here; export will loop from frame 0.

    # ══════════════════════════════════════════════════════════════════
    #  UTILITIES
    # ══════════════════════════════════════════════════════════════════
    def _section_title(self, text):
        title = Text(text, font="Courier New", font_size=16,
                     color=ACCENT, weight=BOLD)
        title.to_edge(UP, buff=0.18)
        bar = Line(title.get_left(), title.get_right(),
                   stroke_color=LASER_COL, stroke_width=1.5)
        bar.next_to(title, DOWN, buff=0.04)
        return VGroup(title, bar)

    def _mini_box(self, label, sublabel, col, pos, w=1.1, h=0.6):
        rect = RoundedRectangle(corner_radius=0.07, width=w, height=h,
                                fill_color=col, fill_opacity=0.12,
                                stroke_color=col, stroke_width=1.8)
        t1 = Text(label,    font="Courier New", font_size=9,
                  color=col, weight=BOLD)
        t2 = Text(sublabel, font="Courier New", font_size=7.5, color=col)
        t2.set_opacity(0.8)
        rect.move_to(pos)
        t1.move_to(np.array(pos) + UP * 0.12)
        t2.move_to(np.array(pos) + DOWN * 0.12)
        return VGroup(rect, t1, t2)

    def _spec_card(self, title_str, rows, color=ACCENT):
        title = Text(title_str, font="Courier New",
                     font_size=11, color=color, weight=BOLD)
        items = VGroup(*[
            Text(f"  {k:<14}{v}", font="Courier New",
                 font_size=9, color=ACCENT)
            for k, v in rows
        ])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        items.next_to(title, DOWN, buff=0.12, aligned_edge=LEFT)
        bg = SurroundingRectangle(
            VGroup(title, items), buff=0.18,
            fill_color=BG, fill_opacity=0.85,
            stroke_color=color, stroke_width=1.5,
            corner_radius=0.1
        )
        return VGroup(bg, title, items)