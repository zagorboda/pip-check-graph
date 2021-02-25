import asyncio
import time
import subprocess
from itertools import chain


async def count(l):

    print('Collecting package {}'.format(l))

    dependencies = dict()
    package = l

    package_process = subprocess.Popen(['pip3', 'show', package], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    await asyncio.sleep(1)
    stdout, _stderr = package_process.communicate(b'\n')

    package_process.terminate()

    dep_list = stdout.split(b'\n')[-3:-1]
    requires = list(filter(lambda x: x, dep_list[0].split(b': ')[1].split(b', ')))
    required_by = list(filter(lambda x: x, dep_list[1].split(b': ')[1].split(b', ')))
    dependencies[package] = {'required_by': '', 'requires': ''}

    dependencies[package]['required_by'] = [x.decode('utf-8') for x in required_by]
    dependencies[package]['requires'] = [x.decode('utf-8') for x in requires]

    return dependencies


async def main(l):
    coros = [count(dep) for dep in l]
    # loop = asyncio.get_event_loop()
    # await loop.run_in_executor(None, count(l))
    list_of_dependencies = await asyncio.gather(*coros)

    all_dependencies = dict(chain.from_iterable(d.items() for d in list_of_dependencies))
    return all_dependencies


if __name__ == "__main__":
    process = subprocess.run(['pip3', 'list'],
                             # capture_output=True,
                             check=True,
                             timeout=60,
                             stdout=subprocess.PIPE).stdout
    a = list(x.split()[0] for x in process.decode("utf-8").split('\n')[2:-1])

    s = time.perf_counter()
    b = asyncio.run(main(a))
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

    dependencies = {k: v for k, v in sorted(b.items(), key=lambda item: len(item[1]))}

    V = len(dependencies)

    edges_list = []

    import networkx as nx

    G = nx.DiGraph()

    for key, value in dependencies.items():
        _required_by, _requires = value['required_by'], value['requires']
        G.add_node(key)
        for item in _requires:
            edges_list.append((key, item))
            G.add_edge(item, key)
        if _required_by:
            print('   {}'.format(', '.join(_required_by)))
            print('  /')
        print(key)
        if _requires:
            print('  \\')
            print('   {}'.format(', '.join(_requires)))
        print('\n')

    import matplotlib.pyplot as plt

    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='r', arrows=True)

    plt.show()
