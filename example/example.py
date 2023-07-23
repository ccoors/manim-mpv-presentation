# -*- coding: utf-8 -*-
import math

from manim import *


class Scene1(Scene):
    CIRCLE_DISTANCE = 2
    CIRCLE_COLORS = [RED, GOLD, BLUE, GREEN, MAROON, PURPLE, ORANGE, TEAL]

    def construct(self):
        txt = MarkupText("Hello <b>World</b>").to_corner(UL)
        txt_end = MarkupText("I am down here").to_corner(DL)
        self.play(Write(txt))
        self.next_section()
        self.play(Transform(txt, txt_end))
        self.next_section()
        circles = [
            Circle()
            .set_fill(self.CIRCLE_COLORS[x], opacity=0.5)
            .set_stroke(self.CIRCLE_COLORS[x])
            for x in range(8)
        ]
        self.play(LaggedStart(*[GrowFromCenter(c) for c in circles]))
        self.play(
            *[
                c.animate.shift(
                    self.CIRCLE_DISTANCE * UP * math.sin(n * math.tau / 8)
                    + self.CIRCLE_DISTANCE * RIGHT * math.cos(n * math.tau / 8)
                )
                for n, c in enumerate(circles)
            ],
            run_time=2,
        )
        self.next_section(type="default.loop")
        obj = Mobject()
        obj.add(*circles)
        self.play(obj.animate.rotate(math.pi / 2))
        self.play(obj.animate.rotate(-math.pi / 2))
        self.next_section()
        self.play(
            LaggedStart(*[Uncreate(c) for c in circles]),
            run_time=2,
        )


class Scene2(Scene):
    def construct(self):
        title = Tex(r"This is some \LaTeX")
        mathtexts = [
            MathTex(r"x^n + y^n = z^n"),
            MathTex(r"\alpha \beta \gamma \theta \lambda \pi \psi \omega"),
            MathTex(r"\infty \forall \exists \square"),
        ]
        VGroup(title, *mathtexts).arrange(DOWN)
        self.play(Write(title), *[Write(m) for m in mathtexts], run_time=3)
