import json
import os
import pprint

with open(os.path.join("data", "videos.json")) as json_file:
    videos = json.load(json_file)

print("We have {} videos".format(len(videos)))
print("Data for the first video looks like this:")
pprint.pprint(videos[0])

tags = set()

for video in videos:
    for tag in video["tags"]:
        tags.add(tag)

num_tags = len(tags)

print("We have {} unique tags".format(num_tags))

tag_to_index = {tag: index for index, tag in enumerate(tags)}


def vectorize_video_input(video):
    input_vector = [0] * num_tags
    for tag in video["tags"]:
        tag_index = tag_to_index.get(tag, None)
        if tag_index is not None:
            input_vector[tag_index] = 1
    return input_vector


with open(os.path.join("data", "categories.json")) as json_file:
    categories = json.load(json_file)

num_categories = len(categories)

print("We have {} categories:".format(num_categories))
pprint.pprint(categories)

category_id_to_index = {
    category["id"]: index for index, category in enumerate(categories)
}
print('Category id to index in target vector:')
print(category_id_to_index)


def vectorize_video_target(video):
    target_vector = [0] * num_categories
    category_index = category_id_to_index.get(video["target_category_id"], None)
    if category_index is not None:
        target_vector[category_index] = 1
    return target_vector


import numpy as np

input_vectors = [vectorize_video_input(video) for video in videos]
target_vectors = [vectorize_video_target(video) for video in videos]

input_vectors = np.array(input_vectors)
target_vectors = np.array(target_vectors)

training_input_vectors = input_vectors[0:200]
training_target_vectors = target_vectors[0:200]
validation_input_vectors = input_vectors[200:]
validation_target_vectors = target_vectors[200:]

from keras.layers.core import Dense
from keras.models import Sequential
from keras.optimizers import SGD

num_hidden_nodes = 20
model = Sequential()
model.add(Dense(num_hidden_nodes, input_dim=num_tags, activation="relu"))
model.add(Dense(num_categories, activation="softmax"))

model.compile(
    loss="categorical_crossentropy", optimizer=SGD(momentum=0.9), metrics=["accuracy"]
)

model.fit(training_input_vectors, training_target_vectors, epochs=100)

evaluation_scores = model.evaluate(validation_input_vectors, validation_target_vectors)

for i, metric_name in enumerate(model.metrics_names):
    print("Validation {}: {:.3f}".format(metric_name, evaluation_scores[i]))
