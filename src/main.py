"""
Simulates a scenario where a person is called to enter a room with two boxes. Box 1 has an x amount of money in it and box two is a mystery box. There is a computer that will predict what the person that comes into the room will pick with a high accuracy. The computer makes its prediction before you walk in. If the computer predicts that you will choose the mystery box alone, it will populate the mystery box with an amount y that is way larger than x (y >> x). If the computer predicts that you will take both boxes, it populates the mystery box with an amount z smaller than x (usually 0). There is no picking just box 1.
----------
todo fill this
Contains:

    Person (class):
        Represents a single person in the problem known as (todo insert problem). The problem is a scenario where a person is called to enter a room with two boxes. Box 1 has an x amount of money in it and box two is a mystery box. There is a computer that will predict what the person that comes into the room will pick with a high accuracy. The computer makes its prediction before you walk in. If the computer predicts that you will choose the mystery box alone, it will populate the mystery box with an amount y that is way larger than x (y >> x). If the computer predicts that you will take both boxes, it populates the mystery box with an amount z smaller than x (usually 0). There is no picking just box 1.
        ----------
        Arguments:
            chance: Callable = random, A function that determines the chance that the person chooses option 1 (the option with the one box mystery). Must return a float in [0, 1)
        ----------
        Attributes:
            Instance:
                one: float, The chance that the person chooses option 1 (the option with the one box mystery)
                two: float, The chance that the person chooses option 2 (the option with both boxes)
                currency: int, The money the person has
                ROI: list[int], Stands for return on investment. A data structure to keep track of the evolution of the person currency over time
                differences: list[int] A data structure to keep track of the change in evolution of the person currency over time
                choices: list[int], A data structure to keep track of the choices the person has made once in the room
        ----------
        Methods:
            Instance:
                choose, Performs the choice for the person
                track, Adds the current currency to a data structure to keep tack of money of time
                plot, Plots the persons statistics. Includes: The change in the person currency over time, their strategy (chances), the relative change in currency over time

    Simulation (class):

    predict (function): Simulates the computer that predicts what a person will pick and populates the box

    main (function): Calls the script's functionality with command line inputs
"""
# pyright: basic
from argparse import Namespace
from collections.abc import Callable
from math import ceil
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.pyplot import subplots, show
from numpy import array, ndarray
from os import makedirs
from os.path import exists, dirname, abspath
from random import random
from utils import liner
from typing import override
# from tqdm import tqdm

# There is redundancy in the implementation I just don't care
class Person:
    """
    Represents a single person in the problem known as (todo insert problem). The problem is a scenario where a person is called to enter a room with two boxes. Box 1 has an x amount of money in it and box two is a mystery box. There is a computer that will predict what the person that comes into the room will pick with a high accuracy. The computer makes its prediction before you walk in. If the computer predicts that you will choose the mystery box alone, it will populate the mystery box with an amount y that is way larger than x (y >> x). If the computer predicts that you will take both boxes, it populates the mystery box with an amount z smaller than x (usually 0). There is no picking just box 1.
    ----------
    Arguments:
        chance: Callable = random, A function that determines the chance that the person chooses option 1 (the option with the one box mystery). Must return a float in [0, 1)
    ----------
    Attributes:
        Instance:
            one: float, The chance that the person chooses option 1 (the option with the one box mystery)
            two: float, The chance that the person chooses option 2 (the option with both boxes)
            currency: int, The money the person has
            ROI: list[int], Stands for return on investment. A data structure to keep track of the evolution of the person currency over time
            differences: list[int] A data structure to keep track of the change in evolution of the person currency over time
            choices: list[int], A data structure to keep track of the choices the person has made once in the room
    ----------
    Methods:
        Instance:
            choose, Performs the choice for the person
            track, Adds the current currency to a data structure to keep tack of money of time
            plot, Plots the persons statistics. Includes: The change in the person currency over time, their strategy (chances), the relative change in currency over time
    """

    def __init__(
        self,
        chance: Callable = random,
    ) -> None:
        """
        Defines:
            one: float, The chance that the person chooses option 1 (the option with the one box mystery)
            two: float, The chance that the person chooses option 2 (the option with both boxes)
            currency: int, The money the person has
            ROI: list[int], Stands for return on investment. A data structure to keep track of the evolution of the person currency over time
            differences: list[int] A data structure to keep track of the change in evolution of the person currency over time
            choices: list[int], A data structure to keep track of the choices the person has made once in the room
        """
        self.one: float = chance()
        """The chance that the person chooses option 1 (the option with the one box mystery)"""
        self.two: float = 1 - self.one
        """The chance that the person chooses option 2 (the option with both boxes)"""
        self.currency: int = 0
        """The money the person has"""
        self.ROI: list[int] = [self.currency]
        """Stands for return on investment. A data structure to keep track of the evolution of the person currency over time"""
        self.differences: list[int] = []
        """A data structure to keep track of the change in evolution of the person currency over time"""
        self.choices: list[int] = []
        """A structure that keeps track of the decisions made by the person"""

    def __str__(self) -> str:
        """
        Defines the value returned when the class is converted to a string
        ----------
        Returns:
            output: str, The string representation of the hash of the object
        """
        return str(self.__hash__())

    @override
    def __hash__(self) -> int:
        """
        Defines a way to assign a unique hash index to the object
        ----------
        Returns:
            output: int, The hash value
        """
        return id(self)

    def choose(self) -> int:
        """
        Performs the choice for the person
        ----------
        Returns:
            output: int, 1 if the person chooses the mystery box (box 2), 2 if they choose both boxes
        """
        key: float = random()
        if key > self.one:
            self.choices.append(2)
            return 2
        else:
            self.choices.append(1)
            return 1

    def track(self) -> None:
        """
        Adds the current currency to a data structure to keep tack of money of time
        ----------
        Returns:
            output: None
        """
        self.ROI.append(self.currency)
        self.differences.append(self.ROI[-1] - self.ROI[-2])

    def plot(
        self,
        components: list[str] = [
            'chances',
            'choices',
            'differences',
            'ROI',
        ],
        present: bool = False,
        output: str = '',
        name: str = 'person.png',
        save: bool = False
    ) -> None:
        """
        Plots the persons statistics. Includes: The change in the person currency over time, their strategy (chances), the relative change in currency over time
        ----------
        Arguments:
            components: list[str] = [
                'chances',
                'ROI',
                'differences',
                'choices',
            ], A set of plots to present in the common plot. Options include chances (presents a bar chart of the persons strategy), ROI (Presents the evolution of the person currency over time), differences (the change in currency between steps), choices (The history of choiecs made by the person)
            present: bool = False, Toggle presenting the image in a matplotlib GUI
            output: str = '', An output directory to dump the image to if saving is enabled (please add a trailing / yourself)
            name: str = 'person.png', An output filename to dump the image to if saving is enabled (should contain the file extension)
            save: bool = False, Toggle saving to a file
        ----------
        Returns:
            output: None
        """
        n: int = len(components)
        rows: int = 1
        cols: int = n
        while rows < cols or rows * cols < n:
            rows += 1
            cols = ceil(n/rows)
        holder: tuple[Figure, Axes] = subplots(rows, cols, figsize=(6 * cols, 6 * rows))
        fig: Figure = holder[0]
        fig.subplots_adjust(wspace = 0.1 * cols, hspace = 0.1 * rows)
        axes: ndarray = array(holder[1]).flatten()
        lb: str  = str(self.__hash__())
        for idx, component in enumerate(components):
            ax: Axes = axes[idx]
            if component == 'choices':
                ax.scatter(range(len(self.choices)), self.choices)
                ax.set_ylim((-0.5, 2.5))
                ax.set_title('Choices')
                ax.set_xlabel('Step')
                ax.set_ylabel('Choice')
                ax.grid()
            if component == 'chances':
                ax.scatter(('Mystery only', 'Both boxes'), (self.one, self.two), label = lb)
                ax.set_ylim((-0.5, 1.5))
                ax.set_title('Chances')
                ax.set_xlabel('Choice')
                ax.set_ylabel('Probability')
                ax.grid()
            if component == 'ROI':
                ax.bar(range(len(self.ROI)), self.ROI)
                ax.set_title('Return On Investment')
                ax.set_xlabel('Step')
                ax.set_ylabel('Money')
                ax.grid()
            if component == 'differences':
                ax.scatter(range(len(self.differences)), self.differences)
                ax.set_ylim(-0.5)
                ax.set_title('Change in money over time')
                ax.set_xlabel('Step (0: between step 0 and 1)')
                ax.set_ylabel('Change')
                ax.grid()
        fig.legend()
        if present:
            show()
        if save:
            makedirs(output, exist_ok=True)
            final: str = output + name
            fig.savefig(final)
            assert exists(final)

# The function has to be placed here so that Person is defined and so that Simulation can take the function as a default argument
def predict(p: Person) -> int:
    """
    Simulates the computer that predicts what a person will pick and populates the box
    ----------
    Note: Will not populate the boxes
    ----------
    Arguments:
        p: Person
    ----------
    Returns:
        output: int, The prediction. 1 indicates the single mystery box will be picked, 2 that both will be picked.
    """
    if p.one > p.two:
        return 1
    else:
        return 2

class Simulation:
    """
    Performs the full simulation of the problem (todo add problem name here).
    ----------
    Arguments:
        x: int = 1000, The amount of money in box 1 (revealed box)
        y: int = 100000, The amount of money in box 2 (mystery box) when box 2 is the single pick
        z: int = 0, The amount of money in box 2 (mystery box) when both box 1 and 2 are picked together
        people: int = 1, How many people to simulate
        chances: Callable = random, A function that should take no inputs that determines a sequential assignment of probabilities of a person picking just box 2 alone (mystery box)
        robot: Callable = predict, A functions on how the robot predicts. Should take a single input, the person (from the Person class or an object with a self.one and self.two attribute)
    ----------
    Attributes:
        Instance:
            x: int, The amount of money in box 1 (revealed box)
            y: int, The amount of money in box 2 (mystery box) when box 2 is the single pick
            z: int, The amount of money in box 2 (mystery box) when both box 1 and 2 are picked together
            chances: Callable, A function that should take no inputs that determines a sequential assignment of probabilities of a person picking just box 2 alone (mystery box)
            n: int, How many people are partaking in the simulation
            people: ndarray, An array of individuals in the simulation
            predictor: Callable, A functions on how the robot predicts. Should take a single input, the person (from the Person class or an object with a self.one and self.two attribute)
            labels: list[list[int]], A data structure to hold the predictions made for each person for each step
            tp: int = 0, True positives
            fp: int = 0, False positives
            tn: int = 0, True negatives
            fn: int = 0, False negatives
    ----------
    Methods:
        Instance:
            populate: Populates the boxes with money
            step: Does a single simulation cycle for all the people in the simulation
            plot: Plots key insights about the people and the steps simulated
    """

    def __init__(
        self,
        x: int = 1000,
        y: int = 1000000,
        z: int = 0,
        people: int = 1,
        chances: Callable = random,
        robot: Callable = predict,
    ) -> None:
        """
        Defines:
            x: int, The amount of money in box 1 (revealed box)
            y: int, The amount of money in box 2 (mystery box) when box 2 is the single pick
            z: int, The amount of money in box 2 (mystery box) when both box 1 and 2 are picked together
            chances: Callable, A function that should take no inputs that determines a sequential assignment of probabilities of a person picking just box 2 alone (mystery box)
            n: int, How many people are partaking in the simulation
            people: ndarray, An array of individuals in the simulation
            predictor: Callable, A functions on how the robot predicts. Should take a single input, the person (from the Person class or an object with a self.one and self.two attribute)
            labels: list[list[int]], A data structure to hold the predictions made for each person for each step
            tp: int = 0, True positives
            fp: int = 0, False positives
            tn: int = 0, True negatives
            fn: int = 0, False negatives
        """
        self.x: int = x
        """The amount of money in box 1 (revealed box)"""
        self.y: int = y
        """The amount of money in box 2 (mystery box) when box 2 is the single pick"""
        self.z: int = z
        """The amount of money in box 2 (mystery box) when both box 1 and 2 are picked together"""
        self.chances: Callable = chances
        """A function that should take no inputs that determines a sequential assignment of probabilities of a person picking just box 2 alone (mystery box)"""
        self.n: int = people
        """How many people are partaking in the simulation"""
        self.people: ndarray = array(
            [
                Person(chance = self.chances) for _ in range(self.n)
            ],
            dtype = Person
        )
        """An array of individuals in the simulation"""
        self.predictor: Callable = robot
        """A functions on how the robot predicts. Should take a single input, the person (from the Person class or an object with a self.one and self.two attribute)"""
        self.labels: list[list[int]] = [[0] * self.n]
        """A data structure to hold the predictions made for each person for each step"""
        self.tp: int = 0
        """True positives"""
        self.fp: int = 0
        """False positives"""
        self.tn: int = 0
        """True negatives"""
        self.fn: int = 0
        """False negatives"""

    def populate(
        self,
        pred: int,
    ) -> tuple[int, int]:
        """
        Populates the boxes with money
        ----------
        Arguments:
            pred: int, The prediction made by the robot
        ----------
        Returns:
            output: tuple[int, int], The boxes arranged like (box 1 (revealed box), box 2 (mystery box))
        """
        if pred == 1:
            return (0, self.y)
        else:
            return (self.x, self.z)

    def step(self) -> None:
        """
        Does a single simulation cycle for all the people in the simulation
        ----------
        Returns:
            output: None
        """
        for person in self.people:
            pred: int = self.predictor(person)
            self.labels[-1].append(pred)
            boxes: tuple[int, int] = self.populate(pred)
            actual: int = person.choose()
            if pred == actual == 1:
                self.tp += 1
            elif pred == actual == 2:
                self.tn += 1
            elif pred == 1 and actual == 2:
                self.fp += 1
            else:
                self.fn += 1
            if actual == 1:
                person.currency += boxes[1]
            else:
                person.currency += boxes[0] + boxes[1]
            person.track()
        self.labels.append([0] * self.n)

    def plot(
        self,
        components: list[str] = [
            'chances',
            'choices',
            'differences',
            'ROI',
            # 'predictions',
        ],
        present: bool = False,
        output: str = '',
        name: str = 'simulation.png',
        save: bool = False
    ) -> None:
        """
        Plots the persons statistics. Includes: The change in the person currency over time, their strategy (chances), the relative change in currency over time
        ----------
        Arguments:
            components: list[str] = [
                'chances',
                'choices',
                'differences',
                'ROI',
                'predictions',
            ], A set of plots to present in the common plot. Options include chances (presents a bar chart of the persons strategy), ROI (Presents the evolution of the person currency over time), differences (the change in currency between steps), predictions (The robot's choices), choices (the choice people made at each step)
            present: bool = False, Toggle presenting the image in a matplotlib GUI
            output: str = '', An output directory to dump the image to if saving is enabled (please add a trailing / yourself)
            name: str = 'simulation.png', An output filename to dump the image to if saving is enabled (should contain the file extension)
            save: bool = False, Toggle saving to a file
        ----------
        Returns:
            output: None
        """
        n: int = len(components)
        rows: int = 1
        cols: int = n
        while rows < cols or rows * cols < n:
            rows += 1
            cols = ceil(n/rows)
        holder: tuple[Figure, Axes] = subplots(rows, cols, figsize=(6 * cols, 6 * rows))
        fig: Figure = holder[0]
        fig.subplots_adjust(wspace = 0.1 * cols, hspace = 0.1 * rows)
        axes: ndarray = array(holder[1]).flatten()
        for idx, component in enumerate(components):
            ax: Axes = axes[idx]
            if component == 'predictions':
                pass
            if component == 'choices':
                domain: range = range(len(self.people[0].choices))
                for person in self.people:
                    ax.scatter(domain, person.choices, alpha = 0.4)
                ax.set_ylim((0.9, 2.1))
                ax.set_title('Choices')
                ax.set_xlabel('Step')
                ax.set_ylabel('Choice')
                ax.grid()
            if component == 'chances':
                marks: list[int] = [0, 1]
                labels = ['Mystery only', 'Both boxes']
                for person in self.people:
                    ax.scatter(
                        marks,
                        [person.one, person.two],
                        alpha=0.4
                    )
                ax.set_xticks(marks)
                ax.set_xticklabels(labels)
                ax.set_ylim((-0.05, 1.05))
                ax.set_title('Chances')
                ax.set_xlabel('Choice')
                ax.set_ylabel('Probability')
                ax.grid()
            if component == 'ROI':
                domain = range(len(self.people[0].ROI))
                for person in self.people:
                    ax.plot(domain, person.ROI, label = person.__hash__())
                ax.set_title('Return On Investment')
                ax.set_xlabel('Step')
                ax.set_ylabel('Money')
                ax.grid()
            if component == 'differences':
                domain = range(len(self.people[0].differences))
                for person in self.people:
                    ax.scatter(domain, person.differences, alpha = 0.4)
                ax.set_ylim(-0.5)
                ax.set_title('Change in money over time')
                ax.set_xlabel('Step (0: between step 0 and 1)')
                ax.set_ylabel('Change')
                ax.grid()
        # fig.legend()
        if present:
            show()
        if save:
            makedirs(output, exist_ok=True)
            final: str = output + name
            fig.savefig(final)
            assert exists(final)

def main() -> None:
    """
    Calls the script's functionality with command line inputs
    ----------
    Returns:
        output: None
    """
    cmd: Namespace = liner()
    sim: Simulation = Simulation(cmd.x, cmd.y, cmd.z, cmd.people, robot = predict)
    for _ in range(cmd.steps):
        sim.step()
    sim.plot(
        output = abspath(
            dirname(
                dirname(
                    __file__
                )
            )
        ) + '/output/',
        name = 't1.png',
        save = True
    )

if __name__ == "__main__":
    main()
