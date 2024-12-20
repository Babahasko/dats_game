import plotly.graph_objs as go

def create_data_for_visualize(snakes, fences, food, enemies, special_food):
    data = []
    # Рисуем змеек
    for snake in snakes:
        x, y, z = zip(*snake['geometry'])
        data.append(go.Scatter3d(x=x, y=y, z=z, mode='lines+markers', name=f"Snake {snake['id']}"))

    # Рисуем препятствия
    x, y, z = zip(*fences)
    data.append(go.Scatter3d(x=x, y=y, z=z, mode='markers', name='Fences', marker=dict(size=5, color='red')))

    # Рисуем еду
    for f in food:
        x, y, z = f['c']
        data.append(go.Scatter3d(x=[x], y=[y], z=[z], mode='markers', name='Food', marker=dict(size=5, color='green')))

    # Рисуем врагов
    for enemy in enemies:
        x, y, z = zip(*enemy['geometry'])
        data.append(go.Scatter3d(x=x, y=y, z=z, mode='lines+markers', name=f"Enemy {enemy['status']}"))

    # Рисуем специальную еду
    for sf in special_food['golden']:
        x, y, z = sf
        data.append(
            go.Scatter3d(x=[x], y=[y], z=[z], mode='markers', name='Special Food', marker=dict(size=5, color='yellow')))

    figure = {
        'data': data,
        'layout': go.Layout(
            scene=dict(
                xaxis=dict(title='X'),
                yaxis=dict(title='Y'),
                zaxis=dict(title='Z')
            ),
            margin=dict(l=0, r=0, b=0, t=0)
        )
    }
    return figure