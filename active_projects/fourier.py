from helpers import *


from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from animation.continual_animation import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.fractals import *
from topics.number_line import *
from topics.combinatorics import *
from topics.numerals import *
from topics.three_dimensions import *
from topics.objects import *
from topics.probability import *
from topics.complex_numbers import *
from scene import Scene
from scene.reconfigurable_scene import ReconfigurableScene
from scene.zoomed_scene import *
from camera import Camera
from mobject import *
from mobject.image_mobject import *
from mobject.vectorized_mobject import *
from mobject.svg_mobject import *
from mobject.tex_mobject import *
from topics.graph_scene import *

#revert_to_original_skipping_status

class AddingPureFrequencies(PiCreatureScene):
    CONFIG = {
        "A_frequency" : 2.1,
        "A_color" : YELLOW,
        "D_color" : PINK,
        "F_color" : TEAL,
        "C_color" : RED,
        "sum_color" : GREEN,
        "equilibrium_height" : 1.5,
    }
    def construct(self):
        self.add_speaker()
        self.play_A440()
        self.measure_air_pressure()
        self.play_lower_pitch()
        self.play_mix()
        self.separate_out_parts()
        self.draw_sum_at_single_point()
        self.draw_full_sum()
        self.add_more_notes()

    def add_speaker(self):
        speaker = SVGMobject(file_name = "speaker")
        speaker.to_edge(DOWN)

        self.add(speaker)
        self.speaker = speaker

    def play_A440(self):
        randy = self.pi_creature
        A_label = TextMobject("A440")
        A_label.highlight(self.A_color)
        A_label.next_to(self.speaker, UP)

        self.broadcast(
            FadeIn(A_label),
            Succession(
                ApplyMethod, randy.change, "pondering",
                Animation, randy,
                Blink, randy
            )
        )

        self.set_variables_as_attrs(A_label)

    def measure_air_pressure(self):
        randy = self.pi_creature
        axes = Axes(
            y_min = -2, y_max = 2,
            x_min = 0, x_max = 10,
            number_line_config = {"include_tip" : False},
        )
        axes.stretch_to_fit_height(2)
        axes.to_corner(UP+LEFT)
        axes.shift(LARGE_BUFF*DOWN)
        eh = self.equilibrium_height
        equilibrium_line = DashedLine(
            axes.coords_to_point(0, eh),
            axes.coords_to_point(axes.x_max, eh),
            stroke_width = 2,
            stroke_color = LIGHT_GREY
        )

        frequency = self.A_frequency
        graph = self.get_wave_graph(frequency, axes)
        func = graph.underlying_function
        graph.highlight(self.A_color)
        pressure = TextMobject("Pressure")
        time = TextMobject("Time")
        for label in pressure, time:
            label.scale_in_place(0.8)
        pressure.next_to(axes.y_axis, UP)
        pressure.to_edge(LEFT, buff = MED_SMALL_BUFF)
        time.next_to(axes.x_axis.get_right(), DOWN+LEFT)
        axes.labels = VGroup(pressure, time)

        n = 10
        brace = Brace(Line(
            axes.coords_to_point(n/frequency, func(n/frequency)),
            axes.coords_to_point((n+1)/frequency, func((n+1)/frequency)),
        ), UP)
        words = brace.get_text("Imagine 440 per second", buff = SMALL_BUFF)
        words.scale(0.8, about_point = words.get_bottom())

        self.play(
            FadeIn(pressure),
            ShowCreation(axes.y_axis)
        )
        self.play(
            Write(time),
            ShowCreation(axes.x_axis)
        )
        self.broadcast(
            ShowCreation(graph, run_time = 4, rate_func = None),
            ShowCreation(equilibrium_line),
        )
        axes.add(equilibrium_line)
        self.play(
            randy.change, "erm", graph,
            GrowFromCenter(brace),
            Write(words)
        )
        self.wait()
        graph.save_state()
        self.play(
            FadeOut(brace),
            FadeOut(words),
            VGroup(axes, graph, axes.labels).shift, 0.8*UP,
            graph.fade, 0.85,
            graph.shift, 0.8*UP,
        )

        graph.saved_state.move_to(graph)
        self.set_variables_as_attrs(axes, A_graph = graph)

    def play_lower_pitch(self):
        axes = self.axes
        randy = self.pi_creature

        frequency = self.A_frequency*(2.0/3.0)
        graph = self.get_wave_graph(frequency, axes)
        graph.set_color(self.D_color)

        D_label = TextMobject("D294")
        D_label.highlight(self.D_color)
        D_label.move_to(self.A_label)

        self.play(
            FadeOut(self.A_label),
            GrowFromCenter(D_label),
        )
        self.broadcast(
            ShowCreation(graph, run_time = 4, rate_func = None),
            randy.change, "happy",
            n_circles = 6,
        )
        self.play(randy.change, "confused", graph)
        self.wait(2)

        self.set_variables_as_attrs(
            D_label,
            D_graph = graph
        )

    def play_mix(self):
        self.A_graph.restore()
        self.broadcast(
            self.get_broadcast_animation(n_circles = 6),
            self.pi_creature.change, "thinking",
            *[
                ShowCreation(graph, run_time = 4, rate_func = None)
                for graph in self.A_graph, self.D_graph
            ]
        )
        self.wait()

    def separate_out_parts(self):
        axes = self.axes
        speaker = self.speaker
        randy = self.pi_creature

        A_axes = axes.deepcopy()
        A_graph = self.A_graph
        A_label = self.A_label
        D_axes = axes.deepcopy()
        D_graph = self.D_graph
        D_label = self.D_label
        movers = [A_axes, A_graph, A_label, D_axes, D_graph, D_label]
        for mover in movers:
            mover.generate_target()
        D_target_group = VGroup(D_axes.target, D_graph.target)
        A_target_group = VGroup(A_axes.target, A_graph.target)
        D_target_group.next_to(axes, DOWN, MED_LARGE_BUFF)
        A_target_group.next_to(D_target_group, DOWN, MED_LARGE_BUFF)
        A_label.fade(1)
        A_label.target.next_to(A_graph.target, UP)
        D_label.target.next_to(D_graph.target, UP)

        self.play(*it.chain(
            map(MoveToTarget, movers),
            [
                ApplyMethod(mob.shift, SPACE_HEIGHT*DOWN, remover = True)
                for mob in  randy, speaker
            ]
        ))
        self.wait()

        self.set_variables_as_attrs(A_axes, D_axes)

    def draw_sum_at_single_point(self):
        axes = self.axes
        A_axes = self.A_axes
        D_axes = self.D_axes
        A_graph = self.A_graph
        D_graph = self.D_graph

        x = 2.85
        A_line = self.get_A_graph_v_line(x)
        D_line = self.get_D_graph_v_line(x)
        lines = VGroup(A_line, D_line)
        sum_lines = lines.copy()
        sum_lines.generate_target()
        self.stack_v_lines(x, sum_lines.target)

        top_axes_point = axes.coords_to_point(x, self.equilibrium_height)
        x_point = np.array(top_axes_point)
        x_point[1] = 0
        v_line = Line(UP, DOWN).scale(SPACE_HEIGHT).move_to(x_point)

        self.revert_to_original_skipping_status()
        self.play(GrowFromCenter(v_line))
        self.play(FadeOut(v_line))
        self.play(*map(ShowCreation, lines))
        self.wait()
        self.play(MoveToTarget(sum_lines, path_arc = np.pi/4))
        self.wait(2)
        self.play(*[
            Transform(
                line, 
                VectorizedPoint(axes.coords_to_point(0, self.equilibrium_height)),
                remover = True
            )
            for line, axes in [
                (A_line, A_axes),
                (D_line, D_axes),
                (sum_lines, axes),
            ]
        ])

    def draw_full_sum(self):
        axes = self.axes

        def new_func(x):
            result = self.A_graph.underlying_function(x)
            result += self.D_graph.underlying_function(x)
            result -= self.equilibrium_height
            return result

        sum_graph = axes.get_graph(new_func)
        sum_graph.highlight(self.sum_color)

        ##TODO
        self.play(
            self.get_graph_line_animation(self.A_axes, self.A_graph),
            self.get_graph_line_animation(self.D_axes, self.D_graph),
            self.get_graph_line_animation(axes, sum_graph.deepcopy()),
            ShowCreation(sum_graph),
            run_time = 15,
            rate_func = None
        )
        self.wait()

        self.sum_graph = sum_graph

    def add_more_notes(self):
        axes = self.axes

        A_group = VGroup(self.A_axes, self.A_graph, self.A_label)
        D_group = VGroup(self.D_axes, self.D_graph, self.D_label)
        squish_group = VGroup(A_group, D_group)
        squish_group.generate_target()
        squish_group.target.stretch(0.5, 1)
        squish_group.target.next_to(axes, DOWN, buff = -SMALL_BUFF)
        for group in squish_group.target:
            label = group[-1]
            bottom = label.get_bottom()
            label.stretch_in_place(0.5, 0)
            label.move_to(bottom, DOWN)

        self.play(MoveToTarget(squish_group))

        F_axes = self.D_axes.deepcopy()
        C_axes = self.A_axes.deepcopy()
        VGroup(F_axes, C_axes).next_to(squish_group, DOWN)
        F_graph = self.get_wave_graph(self.A_frequency*4.0/5, F_axes)
        F_graph.highlight(self.F_color)
        C_graph = self.get_wave_graph(self.A_frequency*6.0/5, C_axes)
        C_graph.highlight(self.C_color)

        F_label = TextMobject("F349")
        C_label = TextMobject("C523")
        for label, graph in (F_label, F_graph), (C_label, C_graph):
            label.scale(0.5)
            label.highlight(graph.get_stroke_color())
            label.next_to(graph, UP, SMALL_BUFF)

        graphs = [self.A_graph, self.D_graph, F_graph, C_graph]
        def new_sum_func(x):
            result = sum([
                graph.underlying_function(x) - self.equilibrium_height
                for graph in graphs
            ])
            result *= 0.5
            return result + self.equilibrium_height
        new_sum_graph = self.axes.get_graph(
            new_sum_func, 
            num_graph_points = 200
        )
        new_sum_graph.highlight(BLUE_C)

        self.play(*it.chain(
            map(ShowCreation, [F_axes, C_axes, F_graph, C_graph,]),
            map(Write, [F_label, C_label]),
            [FadeOut(self.sum_graph)]
        ))
        kwargs = {"rate_func" : None, "run_time" : 10}
        self.play(ShowCreation(new_sum_graph.copy(), **kwargs), *[
            self.get_graph_line_animation(curr_axes, graph, **kwargs)
            for curr_axes, graph in [
                (self.A_axes, self.A_graph),
                (self.D_axes, self.D_graph),
                (F_axes, F_graph),
                (C_axes, C_graph),
                (axes, new_sum_graph),
            ]
        ])
        self.wait()

    ####

    def broadcast(self, *added_anims, **kwargs):
        self.play(self.get_broadcast_animation(**kwargs), *added_anims)

    def get_broadcast_animation(self, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 5)
        kwargs["n_circles"] = kwargs.get("n_circles", 10)
        return Broadcast(self.speaker[1], **kwargs)

    def get_wave_graph(self, frequency, axes):
        tail_len = 3.0
        x_min, x_max = axes.x_min, axes.x_max
        def func(x):
            value = 0.7*np.cos(2*np.pi*frequency*x)
            if x - x_min < tail_len:
                value *= smooth((x-x_min)/tail_len)
            if x_max - x < tail_len:
                value *= smooth((x_max - x )/tail_len)
            return value + self.equilibrium_height
        ngp = 2*(x_max - x_min)*frequency + 1
        graph = axes.get_graph(func, num_graph_points = ngp)
        return graph

    def get_A_graph_v_line(self, x):
        return self.get_graph_v_line(x, self.A_axes, self.A_graph)

    def get_D_graph_v_line(self, x):
        return self.get_graph_v_line(x, self.D_axes, self.D_graph)

    def get_graph_v_line(self, x, axes, graph):
        result = Line(
            axes.coords_to_point(x, self.equilibrium_height),
            # axes.coords_to_point(x, graph.underlying_function(x)),
            graph.point_from_proportion(float(x)/axes.x_max),
            color = WHITE,
            buff = 0,
        )
        return result
    
    def stack_v_lines(self, x, lines):
        point = self.axes.coords_to_point(x, self.equilibrium_height)
        A_line, D_line = lines
        A_line.shift(point - A_line.get_start())
        D_line.shift(A_line.get_end()-D_line.get_start())
        A_line.highlight(self.A_color)
        D_line.highlight(self.D_color)
        return lines

    def create_pi_creature(self):
        return Randolph().to_corner(DOWN+LEFT)

    def get_graph_line_animation(self, axes, graph, **kwargs):
        line = self.get_graph_v_line(0, axes, graph)
        x_max = axes.x_max
        def update_line(line, alpha):
            x = alpha*x_max
            Transform(line, self.get_graph_v_line(x, axes, graph)).update(1)
            return line

        return UpdateFromAlphaFunc(line, update_line, **kwargs)
        
class BreakApartSum(Scene):
    CONFIG = {
        "frequencies" : [0.5, 1.5, 2, 2.5, 5],
        "equilibrium_height" : 2.0,
    }
    def construct(self):
        self.show_initial_sound()
        self.decompose_sound()
        self.ponder_question()

    def show_initial_sound(self):
        def func(x):
            return self.equilibrium_height + 0.2*np.sum([
                np.cos(2*np.pi*f*x)
                for f in self.frequencies
            ])
        axes = Axes(
            x_min = 0, x_max = 5,
            y_min = -1, y_max = 5,
            x_axis_config = {
                "include_tip" : False,
                "unit_size" : 2.0,
            },
            y_axis_config = {
                "include_tip" : False,
                "unit_size" : 0.5,
            },
        )
        axes.stretch_to_fit_width(2*SPACE_WIDTH - 2)
        axes.stretch_to_fit_height(3)
        axes.center()
        axes.to_edge(LEFT)
        graph = axes.get_graph(func, num_graph_points = 200)
        graph.highlight(YELLOW)

        v_line = Line(ORIGIN, 4*UP)
        v_line.move_to(axes.coords_to_point(0, 0), DOWN)
        dot = Dot(color = PINK)
        dot.move_to(graph.point_from_proportion(0))

        self.add(axes, graph)
        self.play(
            v_line.move_to, axes.coords_to_point(5, 0), DOWN,
            MoveAlongPath(dot, graph),
            run_time = 8,
            rate_func = None,
        )
        self.play(*map(FadeOut, [dot, v_line]))

        self.set_variables_as_attrs(axes, graph)

    def decompose_sound(self):
        axes, graph = self.axes, self.graph

        pure_graphs = VGroup(*[
            axes.get_graph(
                lambda x : 0.5*np.cos(2*np.pi*freq*x),
                num_graph_points = 100,
            )
            for freq in self.frequencies
        ])
        pure_graphs.gradient_highlight(BLUE, RED)
        pure_graphs.arrange_submobjects(DOWN, buff = MED_LARGE_BUFF)
        h_line = DashedLine(6*LEFT, 6*RIGHT)

        self.play(
            FadeOut(axes),
            graph.to_edge, UP
        )
        pure_graphs.next_to(graph, DOWN, LARGE_BUFF)
        h_line.next_to(graph, DOWN, MED_LARGE_BUFF)
        self.play(ShowCreation(h_line))
        for pure_graph in reversed(pure_graphs):
            self.play(ReplacementTransform(graph.copy(), pure_graph))
        self.wait()

        self.all_graphs = VGroup(graph, h_line, pure_graphs)
        self.pure_graphs = pure_graphs

    def ponder_question(self):
        all_graphs = self.all_graphs
        pure_graphs = self.pure_graphs
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)

        self.play(
            FadeIn(randy),
            all_graphs.scale, 0.75,
            all_graphs.to_corner, UP+RIGHT,
        )
        self.play(randy.change, "pondering", all_graphs)
        self.play(Blink(randy))
        rect = SurroundingRectangle(pure_graphs, color = WHITE)
        self.play(
            ShowCreation(rect),
            LaggedStart(
                ApplyFunction, pure_graphs,
                lambda g : (lambda m : m.shift(SMALL_BUFF*UP).highlight(YELLOW), g),
                rate_func = wiggle
            )
        )
        self.play(FadeOut(rect))
        self.play(Blink(randy))
        self.wait()

class Quadrant(VMobject):
    CONFIG = {
        "radius" : 2,
        "stroke_width": 0,
        "fill_opacity" : 1,
        "density" : 50,
        "density_exp" : 2.0,
    }
    def generate_points(self):
        points = [r*RIGHT for r in np.arange(0, self.radius, 1./self.density)]
        points += [
            self.radius*(np.cos(theta)*RIGHT + np.sin(theta)*UP)
            for theta in np.arange(0, TAU/4, 1./(self.radius*self.density))
        ]
        points += [r*UP for r in np.arange(self.radius, 0, -1./self.density)]
        self.set_points_smoothly(points)

class UnmixMixedPaint(Scene):
    CONFIG = {
        "colors" : [BLUE, RED, YELLOW, GREEN],
    }
    def construct(self):
        angles = np.arange(4)*np.pi/2
        quadrants = VGroup(*[
            Quadrant().rotate(angle).highlight(color)
            for color, angle in zip(self.colors, angles)
        ])
        quadrants.add(*it.chain(*[
            quadrants.copy().rotate(angle)
            for angle in np.linspace(0, 0.02*TAU, 10)
        ]))
        quadrants.set_fill(opacity = 0.5)

        mud_color = average_color(*self.colors)
        mud_circle = Circle(radius = 2, stroke_width = 0)
        mud_circle.set_fill(mud_color, 1)
        mud_circle.save_state()
        mud_circle.scale(0)

        def update_quadrant(quadrant, alpha):
            points = quadrant.get_anchors()
            dt = 0.03 #Hmm, this has no dependency on frame rate...
            norms = np.apply_along_axis(np.linalg.norm, 1, points)

            points[:,0] -= dt*points[:,1]/np.clip(norms, 0.1, np.inf)
            points[:,1] += dt*points[:,0]/np.clip(norms, 0.1, np.inf)

            new_norms = np.apply_along_axis(np.linalg.norm, 1, points)
            new_norms = np.clip(new_norms, 0.001, np.inf)
            radius = np.max(norms)
            multiplier = norms/new_norms
            multiplier = multiplier.reshape((len(multiplier), 1))
            multiplier.repeat(points.shape[1], axis = 1)
            points *= multiplier
            quadrant.set_points_smoothly(points)

        self.add(quadrants)
        run_time = 30
        self.play(
            *[
                UpdateFromAlphaFunc(quadrant, update_quadrant)
                for quadrant in quadrants
            ] + [
                ApplyMethod(mud_circle.restore, rate_func = None)
            ],
            run_time = run_time
        )

#Incomplete, and probably not useful
class MachineThatTreatsOneFrequencyDifferently(Scene):
    def construct(self):
        graph = self.get_cosine_graph(0.5)
        frequency_mob = DecimalNumber(220, num_decimal_points = 0)
        frequency_mob.next_to(graph, UP, buff = MED_LARGE_BUFF)

        self.graph = graph
        self.frequency_mob = frequency_mob
        self.add(graph, frequency_mob)

        arrow1, q_marks, arrow2 = group = VGroup(
            Vector(DOWN), TextMobject("???").scale(1.5), Vector(DOWN)
        )
        group.highlight(WHITE)
        group.arrange_submobjects(DOWN)
        group.next_to(graph, DOWN)
        self.add(group)

        self.change_graph_frequency(1)
        graph.highlight(GREEN)
        self.wait()
        graph.highlight(YELLOW)
        self.change_graph_frequency(2)
        self.wait()


    def change_graph_frequency(self, frequency, run_time = 2):
        graph = self.graph
        frequency_mob = self.frequency_mob
        curr_frequency = graph.frequency
        self.play(
            UpdateFromAlphaFunc(
                graph, self.get_signal_update_func(graph, frequency),
            ),
            ChangingDecimal(
                frequency_mob, 
                lambda a : 440*interpolate(curr_frequency, frequency, a)
            ),
            run_time = run_time,
        )
        graph.frequency = frequency

    def get_signal_update_func(self, graph, target_frequency):
        curr_frequency = graph.frequency
        def update(graph, alpha):
            frequency = interpolate(curr_frequency, target_frequency, alpha)
            new_graph = self.get_cosine_graph(frequency)
            Transform(graph, new_graph).update(1)
            return graph
        return update

    def get_cosine_graph(self, frequency, num_steps = 200, color = YELLOW):
        result = FunctionGraph(
            lambda x : 0.5*np.cos(2*np.pi*frequency*x),
            num_steps = num_steps
        )
        result.frequency = frequency
        result.shift(2*UP)
        return result

class FourierMachineScene(Scene):
    CONFIG = {
        "time_axes_config" : {
            "x_min" : 0,
            "x_max" : 3.4,
            "x_axis_config" : {
                "unit_size" : 3,
                "tick_frequency" : 0.25,
                "numbers_with_elongated_ticks" : [1, 2, 3],
            },
            "y_min" : 0,
            "y_max" : 2,
            "y_axis_config" : {"unit_size" : 0.8},
        },
        "circle_plane_config" : {
            "x_radius" : 2,
            "y_radius" : 2,
        },
        "text_scale_val" : 0.75,
        "default_graph_config" : {
            "num_graph_points" : 100,
            "color" : YELLOW,
        },
        "equilibrium_height" : 1,
        "default_y_vector_animation_config" : {
            "run_time" : 5,
            "rate_func" : None,
            "remover" : True,
        },
        "default_time_sweep_config" : {
            "rate_func" : None,
            "run_time" : 5,
        },
    }

    def get_time_axes(self):
        time_axes = Axes(**self.time_axes_config)
        time_axes.x_axis.add_numbers()
        time_label = TextMobject("Time")
        intensity_label = TextMobject("Intensity")
        labels = VGroup(time_label, intensity_label)
        for label in labels:
            label.scale(self.text_scale_val)
        time_label.next_to(time_axes.x_axis.get_right(), DOWN)
        intensity_label.next_to(
            time_axes.y_axis.get_top(), RIGHT,
            aligned_edge = UP,
        )
        time_axes.labels = labels
        time_axes.add(labels)
        time_axes.to_corner(UP+LEFT)
        self.time_axes = time_axes
        return time_axes

    def get_circle_plane(self):
        circle_plane = NumberPlane(**self.circle_plane_config)
        circle_plane.to_corner(DOWN+LEFT)
        circle = DashedLine(ORIGIN, TAU*UP).apply_complex_function(np.exp)
        circle.move_to(circle_plane.coords_to_point(0, 0))
        circle_plane.circle = circle
        circle_plane.add(circle)
        circle_plane.fade()
        self.circle_plane = circle_plane
        return circle_plane

    def get_time_graph(self, func, **kwargs):
        if not hasattr(self, "time_axes"):
            self.get_time_axes()
        config = dict(self.default_graph_config)
        config.update(kwargs)
        graph = self.time_axes.get_graph(func, **config)
        return graph

    def get_cosine_wave(self, freq = 1):
        return self.get_time_graph(lambda t : 1 + 0.5*np.cos(TAU*freq*t))

    def get_polarized_mobject(self, mobject, freq = 1.0):
        if not hasattr(self, "circle_plane"):
            self.get_circle_plane()
        polarized_mobject = mobject.copy()
        polarized_mobject.apply_function(lambda p : self.polarize_point(p, freq))
        polarized_mobject.make_smooth()
        mobject.polarized_mobject = polarized_mobject
        polarized_mobject.frequency = freq
        return polarized_mobject

    def polarize_point(self, point, freq = 1.0):
        t, y = self.time_axes.point_to_coords(point)
        z = y*np.exp(complex(0, -2*np.pi*freq*t))
        return self.circle_plane.coords_to_point(z.real, z.imag)

    def get_polarized_animation(self, mobject, freq = 1.0):
        p_mob = self.get_polarized_mobject(mobject, freq = freq)
        def update_p_mob(p_mob):
            Transform(
                p_mob, 
                self.get_polarized_mobject(mobject, freq = freq)
            ).update(1)
            mobject.polarized_mobject = p_mob
            return p_mob
        return UpdateFromFunc(p_mob, update_p_mob)

    def animate_frequency_change(self, mobjects, new_freq, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 3.0)
        added_anims = kwargs.get("added_anims", [])
        self.play(*[
            self.get_frequency_change_animation(mob, new_freq, **kwargs)
            for mob in mobjects
        ] + added_anims)

    def get_frequency_change_animation(self, mobject, new_freq, **kwargs):
        if not hasattr(mobject, "polarized_mobject"):
            mobject.polarized_mobject = self.get_polarized_mobject(mobject)
        start_freq = mobject.polarized_mobject.frequency
        def update(pm, alpha):
            freq = interpolate(start_freq, new_freq, alpha)
            new_pm = self.get_polarized_mobject(mobject, freq)
            Transform(pm, new_pm).update(1)
            mobject.polarized_mobject = pm
            mobject.polarized_mobject.frequency = freq
            return pm
        return UpdateFromAlphaFunc(mobject.polarized_mobject, update, **kwargs)

    def get_time_graph_y_vector_animation(self, graph, **kwargs):
        config = dict(self.default_y_vector_animation_config)
        config.update(kwargs)
        vector = Vector(UP, color = WHITE)
        graph_copy = graph.copy()
        x_axis = self.time_axes.x_axis
        x_min, x_max = x_axis.x_min, x_axis.x_max
        def update_vector(vector, alpha):
            x = interpolate(x_min, x_max, alpha)
            vector.put_start_and_end_on(
                self.time_axes.coords_to_point(x, 0),
                self.time_axes.input_to_graph_point(x, graph_copy)
            )
            return vector
        return UpdateFromAlphaFunc(vector, update_vector, **config)

    def get_polarized_vector_animation(self, polarized_graph, **kwargs):
        config = dict(self.default_y_vector_animation_config)
        config.update(kwargs)
        vector = Vector(RIGHT, color = WHITE)
        origin = self.circle_plane.coords_to_point(0, 0)
        graph_copy = polarized_graph.copy()
        def update_vector(vector, alpha):
            point = graph_copy.point_from_proportion(alpha)
            vector.put_start_and_end_on(origin, point)
            return vector
        return UpdateFromAlphaFunc(vector, update_vector, **config)

    def get_vector_animations(self, graph, draw_polarized_graph = True, **kwargs):
        config = dict(self.default_y_vector_animation_config)
        config.update(kwargs)
        anims = [
            self.get_time_graph_y_vector_animation(graph, **config),
            self.get_polarized_vector_animation(graph.polarized_mobject, **config),
        ]
        if draw_polarized_graph:
            new_config = dict(config)
            new_config["remover"] = False
            anims.append(ShowCreation(graph.polarized_mobject, **new_config))
        return anims

    def animate_time_sweep(self, freq, n_repeats = 1, t_max = None, **kwargs):
        added_anims = kwargs.pop("added_anims", [])
        config = dict(self.default_time_sweep_config)
        config.update(kwargs)
        circle_plane = self.circle_plane
        time_axes = self.time_axes
        ctp = time_axes.coords_to_point
        t_max = t_max or time_axes.x_max
        v_line = DashedLine(
            ctp(0, 0), ctp(0, time_axes.y_max),
        )
        v_line.highlight(RED)

        for x in range(n_repeats):
            v_line.move_to(ctp(0, 0), DOWN)
            self.play(
                ApplyMethod(
                    v_line.move_to, 
                    ctp(t_max, 0), DOWN
                ),
                self.get_polarized_animation(v_line, freq = freq),
                *added_anims,
                **config
            )
            self.remove(v_line.polarized_mobject)
        self.play(FadeOut(VGroup(v_line, v_line.polarized_mobject)))

    def get_v_lines_indicating_periods(self, freq, n_lines = 10):
        period = 1./freq
        v_lines = VGroup(*[
            DashedLine(ORIGIN, 1.5*UP).move_to(
                self.time_axes.coords_to_point(n*period, 0),
                DOWN
            )
            for n in range(1, n_lines + 1)
        ])
        v_lines.set_stroke(LIGHT_GREY)
        return v_lines

class WrapCosineGraphAroundCircle(FourierMachineScene):
    CONFIG = {
        "initial_winding_frequency" : 0.5,
        "signal_frequency" : 3.0,
    }
    def construct(self):
        self.show_initial_signal()
        self.wrap_around_circle()
        self.show_time_sweeps()
        self.compare_two_frequencies()
        self.change_wrapping_frequency()
        self.match_up_frequencies()

    def show_initial_signal(self):
        axes = self.get_time_axes()
        graph = self.get_cosine_wave(freq = self.signal_frequency)
        peak_points = [
            axes.input_to_graph_point(x, graph)
            for x in np.linspace(1, 2, 4)
        ]
        braces = VGroup(*[
            Brace(Line(p1, p2), UP)
            for p1, p2 in zip(peak_points, peak_points[1:])
        ])
        v_lines = VGroup(*[
            DashedLine(
                ORIGIN, 2*UP, color = RED
            ).move_to(axes.coords_to_point(x, 0), DOWN)
            for x in 1, 2
        ])
        words = TextMobject("3 beats/second")
        words.scale_to_fit_width(0.9*braces.get_width())
        words.next_to(braces, UP, SMALL_BUFF)

        self.add(axes)
        self.play(ShowCreation(graph, run_time = 2))
        self.play(
            FadeIn(words),
            *map(ShowCreation, v_lines)
        )
        self.play(LaggedStart(FadeIn, braces))
        self.wait()
        self.play(FadeOut(VGroup(braces, v_lines)))
        self.wait()

        self.beats_per_second_label = words
        self.graph = graph

    def wrap_around_circle(self):
        graph = self.graph
        freq = self.initial_winding_frequency
        low_freq = freq/3
        polarized_graph = self.get_polarized_mobject(graph, low_freq)
        circle_plane = self.get_circle_plane()
        moving_graph = graph.copy()

        self.play(ShowCreation(circle_plane))
        self.play(ReplacementTransform(
            moving_graph,
            polarized_graph,
            run_time = 3,
            path_arc = -TAU/2
        ))
        self.animate_frequency_change([graph], freq)
        self.wait()
        self.play(*self.get_vector_animations(graph), run_time = 15)
        self.wait()

    def show_time_sweeps(self):
        freq = self.initial_winding_frequency
        graph = self.graph

        v_lines = self.get_v_lines_indicating_periods(freq)
        winding_freq_label = VGroup(
            DecimalNumber(freq, num_decimal_points = 2),
            TextMobject("cycles/second")
        )
        winding_freq_label.arrange_submobjects(RIGHT)
        winding_freq_label.next_to(
            self.circle_plane, RIGHT, aligned_edge = UP
        )

        self.animate_time_sweep(
            freq = freq,
            t_max = 4,
            run_time = 6,
            added_anims = [FadeIn(v_lines)]
        )
        self.play(
            FadeIn(winding_freq_label),
            *self.get_vector_animations(graph)
        )
        self.wait()

        self.winding_freq_label = winding_freq_label
        self.v_lines_indicating_periods = v_lines

    def compare_two_frequencies(self):
        bps_label = self.beats_per_second_label
        wps_label = self.winding_freq_label
        for label in bps_label, wps_label:
            label.rect = SurroundingRectangle(
                label, color = RED
            )
        graph = self.graph
        freq = self.initial_winding_frequency

        peak_points = [
            self.time_axes.input_to_graph_point(x, graph)
            for x in np.arange(0, 3.5, 1./self.signal_frequency)
        ]
        braces = VGroup(*[
            Brace(Line(p1, p2), UP, buff = 0)
            for p1, p2 in zip(peak_points, peak_points[1:])
        ])

        self.play(ShowCreation(bps_label.rect))
        self.play(FadeOut(bps_label.rect))
        self.play(LaggedStart(FadeIn, braces, run_time = 3))
        self.play(FadeOut(braces))
        self.play(ShowCreation(wps_label.rect))
        self.play(FadeOut(wps_label.rect))
        self.animate_time_sweep(freq = freq, t_max = 4)
        self.wait()

    def change_wrapping_frequency(self):
        graph = self.graph
        v_lines = self.v_lines_indicating_periods
        freq_label = self.winding_freq_label[0]

        count = 0
        for target_freq in [2, 0.2, 1.55, self.signal_frequency]:
            self.play(
                Transform(
                    v_lines, 
                    self.get_v_lines_indicating_periods(target_freq)
                ),
                ChangeDecimalToValue(freq_label, target_freq),
                self.get_frequency_change_animation(graph, target_freq),
                run_time = 4,
            )
            self.wait()
            if count == 2:
                self.play(LaggedStart(
                    ApplyFunction, v_lines,
                    lambda mob : (
                        lambda m : m.shift(0.25*UP).highlight(YELLOW), 
                        mob
                    ),
                    rate_func = there_and_back
                ))
                self.animate_time_sweep(target_freq, t_max = 2)
            count += 1
        self.wait()
        self.play(
            *self.get_vector_animations(graph, False),
            run_time = 15
        )

    def match_up_frequencies(self):
        pass



























