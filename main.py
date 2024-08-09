from manim import *
from manim_physics import *
import numpy as np
import math

class IndustryStructure(Scene):
    def construct(self):
        numberlineScale = 5
        structureScale = NumberLine(
            x_range=[-1.0,1.0,.1],
            include_numbers=False,
            length=numberlineScale*2,
            decimal_number_config={"num_decimal_places": 1},
            color=DARK_BLUE
        )
        pointer = RegularPolygon(
            n=3, 
            fill_color=WHITE, 
            fill_opacity=1, 
            start_angle=(np.pi/6),
            stroke_width=0
        )
        pointer.scale(.2)
        pointer.set_y(pointer.get_y() + .5)
        tracker = ValueTracker(0)

        monopoly_text = Text("Monopoly", font_size=24)
        monopoly_text.shift(LEFT*numberlineScale + DOWN*.3)

        PerfectComp_text = Text("Perfect Competition", font_size=24)
        PerfectComp_text.shift(RIGHT*numberlineScale + DOWN*.3)

        TitleText = Text("Types of Industries", font_size=36).shift(UP*3)

        pointer.add_updater(lambda x: x.set_x(tracker.get_value()))
        self.add(structureScale, pointer, monopoly_text, PerfectComp_text, TitleText)
        self.play(tracker.animate.set_value(5))
        self.wait(3)
        self.play(tracker.animate.set_value(-5))
        self.wait(3)
        self.play(tracker.animate.set_value(0))
        self.wait(3)
        self.play(tracker.animate.set_value(-3))
        self.wait(3)
        self.play(tracker.animate.set_value(3))
        self.wait(3)
        self.play(tracker.animate.set_value(0))
        self.wait(3)

class ElasticitySteepness(Scene):
    def construct(self):
        numLineScale = 5
        quantity, price = self.setupAxes(numLineScale)
        demandYIntercept = ValueTracker(2)
        demand_endX = ValueTracker(5)
        demand_endY = ValueTracker(quantity.get_y())

        demandLine = Line(
            start=(price.get_x(), demandYIntercept.get_value(), 0),
            end=(demand_endX.get_value(), quantity.get_y(), 0)
        )

        demandLine.add_updater(lambda x: x.put_start_and_end_on(
            (price.get_x(), demandYIntercept.get_value(), 0),
            (demand_endX.get_value(), demand_endY.get_value(), 0)
        ))

        TitleText = Text("Types of Industries", font_size=36).shift(UP*3)

        quantityText = Text("Quantity", font_size=24).shift(DOWN * 3.5)
        priceText = Text("Price", font_size=24).rotate(np.pi/2).shift(LEFT*(numLineScale+.5))

        demandText = Text("Demand", font_size=20)
        demandText.add_updater(lambda x: x.set_x(demandLine.get_center()[0] + .5))
        demandText.add_updater(lambda x: x.set_y(demandLine.get_center()[1] + .25))
        demandText.set_x(0)

        self.add(
            quantity,
            price,
            demandLine,
            quantityText,
            priceText,
            demandText,
            TitleText
        )

        self.play(demand_endX.animate.set_value(5),
                  demand_endY.animate.set_value(0),
                  demandYIntercept.animate.set_value(0))
        self.wait(3)
        self.play(demandYIntercept.animate.set_value(2),
                  demand_endY.animate.set_value(quantity.get_y()),
                  demand_endX.animate.set_value(-3))
        self.wait(3)
        self.play(demandYIntercept.animate.set_value(2),
                  demand_endX.animate.set_value(5))
        self.wait(3)

    def setupAxes(self, numLineScale):
        quantity = NumberLine(
            x_range=[-1.0, 1.0, .1],
            include_numbers=False,
            length=numLineScale*2,
            color=DARK_BLUE
        )
        quantity.shift(DOWN*3)

        price = NumberLine(
            x_range=[-0.5, 0.5, .1],
            include_numbers=False,
            length=numLineScale,
            color=DARK_BLUE
        )
        price.rotate(np.pi/2)
        price.shift(LEFT*numLineScale + DOWN*0.5)

        return quantity, price
    

class EVMarketShare2019(Scene):
    def construct(self):

        colors = [RED, YELLOW, BLUE, GREY_BROWN, DARK_BLUE, GREY]
        pichart = self.createSectors(0.8, 0.07, 0.06, 0.02, 0.02, 0.03, 
                                    colors=colors,
                                    stroke_color=GREY_BROWN,
                                    stroke_width=3,
                                    fill_opacity=1)
        [i.save_state() for i in pichart]

        labels = ["Tesla 80%", "Chevrolet 7%", "Nissan 6%", "Audi 2%", "Volkswagen 2%", "Others 3%"]
        Legend = self.createLegend(colors, labels)

        self.wait(1)
        self.play(Create(
            Text("EV Market Share in 2019", font_size=36).shift(UP*3.5), run_time=0.5
        ))
        self.add(Legend.shift(RIGHT*3 + DOWN))
        self.play(Create(pichart.shift(LEFT*2 + DOWN*.25), lag_ratio=0.5, run_time=5))  
        self.wait(3)

    def createSectors(self, *weights, colors, outerRadius=3, **kwargs):
        sectors = VGroup()
        lastWeight = 0
        for weight, color in zip(weights, colors):
            sectors.add(
                Sector(outer_radius=outerRadius, angle=weight*TAU, start_angle=lastWeight*TAU, color = color,**kwargs)
            )
            # sectors[-1].rotate(lastWeight*TAU, about_point=ORIGIN)
            lastWeight += weight

        return sectors
    def createLegend(self, colors, labels):
        out = VGroup()
        numLabels = len(labels) // 2
        for color, label in zip(colors, labels):
            out.add(Line(LEFT, ORIGIN, stroke_width=5, color=color).shift(UP*numLabels), 
                   Text(label, font_size=20).shift(RIGHT*1.25).shift(UP*numLabels))
            numLabels -= 1
        out.add(SurroundingRectangle(out, color=WHITE))
            
        return out
    
class DemandDeterminants(Scene):
    def construct(self):
        # part 1
        colors = [RED, YELLOW, BLUE, GREY]
        pichart = self.createSectors(0.5, 0.18, 0.15, 0.17, 
                                        colors=colors,
                                        stroke_color=GREY_BROWN,
                                        stroke_width=3,
                                        fill_opacity=1)
        [i.save_state() for i in pichart]
        labels = ["Environment 50%", "Cost Savings 18%", "Performance 15%", "Other 17%"]
        Legend = self.createLegend(colors, labels)

        self.play(Create(
            Text("Demand Determinants", font_size=36).shift(UP*3.5)
        ))
        self.wait(3)
        self.play(Create(pichart.shift(LEFT*3), run_time=5))
        self.add(Legend.shift(RIGHT*3+DOWN*1.2))
        self.wait(3)
        self.play(
            Wiggle(pichart[0], n_wiggles=8, run_time=3, rotation_angle=0.01*PI),
            Wiggle(pichart[2], n_wiggles=8, run_time=3, rotation_angle=0.01*PI)
            )
        self.wait(3)

    def createSectors(self, *weights, colors, outerRadius=3, **kwargs):
            sectors = VGroup()
            lastWeight = 0
            for weight, color in zip(weights, colors):
                sectors.add(
                    Sector(outer_radius=outerRadius, angle=weight*TAU, start_angle=lastWeight*TAU, color = color,**kwargs)
                )
                # sectors[-1].rotate(lastWeight*TAU, about_point=ORIGIN)
                lastWeight += weight

            return sectors
    def createLegend(self, colors, labels):
        out = VGroup()
        numLabels = len(labels) // 2
        for color, label in zip(colors, labels):
            out.add(Line(LEFT, ORIGIN, stroke_width=5, color=color).shift(UP*numLabels), 
                   Text(label, font_size=20).shift(RIGHT*1.25).shift(UP*numLabels))
            numLabels -= 1
        out.add(SurroundingRectangle(out, color=WHITE))
            
        return out
    
class RelatedGoodDemandIncrease(Scene):
    def construct(self):
        demandYInt = ValueTracker(5)
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            tips=False,
            axis_config={"include_numbers": False, "color":DARK_BLUE}
        )
        xLabel = ax.get_x_axis_label(
            Tex("Quantity").scale(0.7), edge=DOWN, direction=DOWN
        )
        yLabel = ax.get_y_axis_label(
            Tex("Price").scale(0.7)
        )
        demandLine = always_redraw(
            lambda: ax.plot(
                lambda x: demandYInt.get_value()-x, 
                x_range=[0,
                        demandYInt.get_value()]
            )
        )
        demandText = Text("Demand", font_size=24).add_updater(
            lambda x: x.move_to(demandLine.get_end() + UP*.75)
        )

        supplyLine = ax.plot(
            lambda x: x, x_range=[0,10]
        )
        supplyText = Text("Supply", font_size=24).move_to(
            supplyLine.get_end() + DOWN * .75
        )
        equilibriumLineX = always_redraw(lambda: DashedVMobject(ax.plot(
            lambda x: demandYInt.get_value() / 2, x_range=[0, demandYInt.get_value() / 2]
        )))
        equilibriumXText = Text("Eq. Price", font_size=20).add_updater(
            lambda x: x.move_to(
                ax.c2p(demandYInt.get_value() / 4 - 0.5, demandYInt.get_value() / 2 + 0.5)
            )
        )

        equilibriumLineY = always_redraw(lambda: DashedVMobject(Line(
            ax.c2p(demandYInt.get_value() / 2, 0, 0), 
            ax.c2p(demandYInt.get_value() / 2, demandYInt.get_value() / 2, 0)
        ), num_dashes=7))
        equilibriumYText = Text("Eq. Quantity", font_size=20).rotate(np.pi/2).add_updater(
            lambda x: x.move_to(
                ax.c2p(demandYInt.get_value() / 2 + 0.3, demandYInt.get_value() / 4 - 0.5)
            )
        )

        iDot = always_redraw(lambda: Dot(
            (ax.c2p(demandYInt.get_value() / 2, demandYInt.get_value() / 2)),
            color=RED
        )
        )
        pricePointer = always_redraw(lambda: Dot(
             ax.c2p(0, demandYInt.get_value() / 2, 0), fill_color=LIGHT_GRAY, fill_opacity=1, stroke_width=0
        ))
        quantityPointer = always_redraw(lambda: Dot(
             ax.c2p(demandYInt.get_value() / 2, 0, 0), fill_color=LIGHT_GRAY, fill_opacity=1, stroke_width=0
        ))

        self.play(Write(ax), Write(
            Text("Changes in Demand", font_size=36).shift(UP*3)
        ))
        self.play(Write(demandLine), Write(supplyLine), Write(xLabel), Write(yLabel), Write(iDot))
        self.play(
            Write(supplyText),
            Write(demandText), 
            Write(pricePointer), 
            Write(quantityPointer), 
            Write(equilibriumLineX), 
            Write(equilibriumLineY),
            Write(equilibriumXText),
            Write(equilibriumYText))
        self.wait(3)
        self.play(demandYInt.animate.set_value(10), run_time=7, lag_ratio=.01)
        self.wait(3)

    def setupAxes(self, numLineScale):
        quantity = NumberLine(
            x_range=[-1.0, 1.0, .1],
            include_numbers=False,
            length=numLineScale*2,
            color=DARK_BLUE
        )
        quantity.shift(DOWN*3)

        price = NumberLine(
            x_range=[-0.5, 0.5, .1],
            include_numbers=False,
            length=numLineScale,
            color=DARK_BLUE
        )
        price.rotate(np.pi/2)
        price.shift(LEFT*numLineScale + DOWN*0.5)

        return quantity, price

class DemandIncreasePriceConstant(Scene):
    def construct(self):
        demandYInt = ValueTracker(7)
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            tips=False,
            axis_config={"include_numbers": False, "color":DARK_BLUE}
        ).shift(DOWN*.25)
        xLabel = ax.get_x_axis_label(
            Tex("Quantity").scale(0.7), edge=DOWN, direction=DOWN
        )
        yLabel = ax.get_y_axis_label(
            Tex("Price").scale(0.7)
        )
        demandLine = always_redraw(
            lambda: ax.plot(
                lambda x: demandYInt.get_value()-x, 
                x_range=[0,
                        demandYInt.get_value()]
            )
        )
        demandText = Text("Demand", font_size=24).add_updater(
            lambda x: x.move_to(demandLine.get_end() + UP*.75)
        )

        equilibriumXText = Text("Firm's Price", font_size=20).move_to(
                ax.c2p(0.7, 5.5)
        )
        equilibriumYText = Text("Quantity Sold", font_size=20).rotate(np.pi/2).add_updater(
            lambda x: x.move_to(
                ax.c2p(demandYInt.get_value() -5 + 0.3, 1.7)
            )
        )
        iDot = always_redraw(lambda: Dot(
            (ax.c2p(demandYInt.get_value() -5, 5)),
            color=RED
        ))
        equilibrium = always_redraw(lambda: ax.get_lines_to_point(
            iDot.get_center(), 
            stroke_width=5
        ))

        
        pricePointer = always_redraw(lambda: Dot(
             ax.c2p(0, 5, 0), fill_color=LIGHT_GRAY, fill_opacity=1, stroke_width=0
        ))
        quantityPointer = always_redraw(lambda: Dot(
             ax.c2p(demandYInt.get_value() - 5, 0, 0), fill_color=LIGHT_GRAY, fill_opacity=1, stroke_width=0
        ))

        self.play(Write(ax), Write(
            Text("Constant Price and Variable Quanitity", font_size=30).shift(UP*3.2)
        ))
        self.play(Write(demandLine), Write(xLabel), Write(yLabel), Write(iDot))
        self.play(
            Write(demandText), 
            Write(pricePointer),
            Write(equilibrium), 
            Write(quantityPointer), 
            Write(equilibriumXText),
            Write(equilibriumYText))
        self.wait(3)
        self.play(demandYInt.animate.set_value(10), run_time=4, lag_ratio=.01)
        self.wait(3)

    def setupAxes(self, numLineScale):
        quantity = NumberLine(
            x_range=[-1.0, 1.0, .1],
            include_numbers=False,
            length=numLineScale*2,
            color=DARK_BLUE
        )
        quantity.shift(DOWN*3)

        price = NumberLine(
            x_range=[-0.5, 0.5, .1],
            include_numbers=False,
            length=numLineScale,
            color=DARK_BLUE
        )
        price.rotate(np.pi/2)
        price.shift(LEFT*numLineScale + DOWN*0.5)

        return quantity, price

class EVMarketShare2024(Scene):
    def construct(self):

        colors = [RED, YELLOW, BLUE, GREY_BROWN, DARK_BLUE, GREY]
        pichart = self.createSectors(0.52, .082, 0.054, 0.046, 0.042, 0.26, 
                                    colors=colors,
                                    stroke_color=GREY_BROWN,
                                    stroke_width=3,
                                    fill_opacity=1)
        [i.save_state() for i in pichart]

        labels = ["Tesla 52%", "Ford 8%", "Hyundai 5%", "Mercedez-Benz 5%", "Rivian 4%", ">16 Others 26%"]
        Legend = self.createLegend(colors, labels)

        self.wait(1)
        self.play(Write(
            Text("EV Market Share in 2024", font_size=36).shift(UP*3.5), run_time=0.5
        ))
        self.play(Write(Legend.shift(RIGHT*3 + DOWN)))
        self.play(
            Create(pichart.shift(LEFT*2 + DOWN*.25), lag_ratio=0.5, run_time=5),
            Write(Dot(color=GREY_BROWN).move_to(pichart.get_center()))
        )  
        self.wait(3)

    def createSectors(self, *weights, colors, outerRadius=3, **kwargs):
        sectors = VGroup()
        lastWeight = 0
        for weight, color in zip(weights, colors):
            sectors.add(
                Sector(outer_radius=outerRadius, angle=weight*TAU, start_angle=lastWeight*TAU, color = color,**kwargs)
            )
            # sectors[-1].rotate(lastWeight*TAU, about_point=ORIGIN)
            lastWeight += weight

        return sectors
    def createLegend(self, colors, labels):
        out = VGroup()
        numLabels = len(labels) // 2
        for color, label in zip(colors, labels):
            out.add(Line(LEFT, ORIGIN, stroke_width=5, color=color).shift(UP*numLabels), 
                   Text(label, font_size=20).shift(RIGHT*1.3).shift(UP*numLabels))
            numLabels -= 1
        out.add(SurroundingRectangle(out, color=WHITE))
            
        return out
    
class NewAndUsedEvs(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            tips=False,
            axis_config={
                "color":DARK_BLUE
            }
        )
        xLabel = ax.get_x_axis_label(
            Text("Time", font_size=24),
            edge=DOWN,
            direction=DOWN
        )
        yLabel = ax.get_y_axis_label(
            Text("Demand", font_size=24)
        )
        t = ValueTracker(0)

        usedEvDemand: ParametricFunction = always_redraw(lambda: ax.plot(
            lambda x: (10*x**2)/(x**2+70), 
            x_range=[0, t.get_value()],
            color=BLUE
        ))
        usedEvDemandPoint = always_redraw(lambda: Dot(
            usedEvDemand.get_function()(t.get_value()),
            color=DARK_BLUE
        ))
        newEvDemand = always_redraw(lambda: ax.plot(
            lambda x: 10-usedEvDemand.underlying_function(x), 
            x_range=[0, t.get_value()],
            color=RED
        ))
        newEvDemandPoint = always_redraw(lambda: Dot(
            newEvDemand.get_function()(t.get_value()),
            color=RED_E
        ))

        legend = self.getLegend([
            "New Evs",
            "Hybrid and Used Evs"
        ], [RED, BLUE], .5).shift(RIGHT*3 + UP*1.7)

        self.wait()
        self.play(
            Write(ax),
            Write(
                Text("The Substitution Effect", font_size=36).\
                shift(UP*3.5)
            ),
            Write(xLabel),
            Write(yLabel)
        )
        self.add(usedEvDemand, newEvDemand)
        self.play(
            Write(legend),
            Write(usedEvDemandPoint), 
            Write(newEvDemandPoint)
        )
        self.play(t.animate.set_value(10))
        self.wait(3)
    def getLegend(self, labels, colors, heightIncrement=0.75):
        legend = VGroup()
        heightOffset = (len(labels) / 2)
        for label, color in zip(labels, colors):
            legend.add(
                VGroup(
                    Text(
                        label,
                        color=color,
                        font_size=20
                    ).shift(RIGHT*.7), Line(
                        LEFT, ORIGIN, color=color, stroke_width=5
                    ).shift(LEFT*.7)
                ).shift(UP * heightOffset * heightIncrement).save_state()
            ).save_state()
            heightOffset -= 1
        legend.add(SurroundingRectangle(
            legend, color=LIGHT_GRAY
        ))
        return legend
    

class LowElasticityPriceChange(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            tips=False,
            axis_config={
                "color":BLUE
            }
        ).shift(DOWN*.3)
        xLabel= ax.get_x_axis_label(
            Text("Quantity", font_size=24),
            edge=DOWN,
            direction=DOWN
        )
        yLabel= ax.get_y_axis_label(
            Text("Price", font_size=24)
        )
        title = VGroup(
            Text("Disproportionate Price Changes", font_size=36),
            Text("Inelastic Demand", font_size=28)
        ).arrange(DOWN, buff=.01).shift(UP*3.5)

        q = ValueTracker(5)

        m = 10
        demand = ax.plot(
            lambda x: 5-m*(x-5), x_range=[-5/m + 5, 5/m + 5]
        )

        marketPoint = always_redraw(lambda: Dot(
            ax.c2p(q.get_value(), demand.underlying_function(q.get_value())),
            color=YELLOW_C
        ))
        eqLines = always_redraw(lambda: ax.get_lines_to_point(
            ax.c2p(q.get_value(), demand.underlying_function(q.get_value())),
            color=GREEN
        ))
        eqLines[0].add_updater(lambda x: x.set_color(GREEN))
        eqLines[1].add_updater(lambda x: x.set_color(RED))

        qPoint = always_redraw(lambda: Dot(
            eqLines[1].get_start(),
            color=RED
        ))
        pPoint = always_redraw(lambda: Dot(
            eqLines[0].get_start(),
            color=GREEN
        ))





        self.play(Write(title))
        self.play(
            Write(ax),
            Write(xLabel),
            Write(yLabel)
        )
        self.play(
            Write(demand),
            Write(marketPoint),
            Write(eqLines),
            Write(qPoint),
            Write(pPoint)
        )
        self.play(q.animate.increment_value(.1))
        self.play(q.animate.increment_value(-.2))
        self.play(q.animate.increment_value(.1))



