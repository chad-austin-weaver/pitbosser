import matplotlib.pyplot as plt
import pandas as pd


def generate_game_mix_chart(game_mix):

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:

    labels = [x for x in game_mix.keys() if game_mix[x] != 0]
    sizes = [x for x in game_mix.values() if x != 0]
    sorted_data = sorted(zip(sizes, labels), reverse=True)
    sizes, labels = zip(*sorted_data)

    fig, ax = plt.subplots()
    patches, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_facecolor('none')
    fig.patch.set_facecolor('none')
    [text.set_color('white') for text in texts]
    return fig


def generate_schedule(solution):
    df = pd.DataFrame({
        "table": solution.keys(),
        "dealer": solution.values()
    })
    return df


def generate_test_cases_chart():
    # Bar charts for test cases.
    fig, ax = plt.subplots()

    percentages = ['0-30%', '40%', '50%', '60%', '70%', '80-100%']
    counts = [0, 5, 31, 65, 93, 100]

    ax.bar(percentages, counts)

    ax.set_ylabel('Percentage of found solutions at n% known games')
    ax.set_title('Random unit test aggregate results')

    plt.savefig("unit_tests/test_results_chart")
