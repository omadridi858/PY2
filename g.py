import insightface
import numpy as np
import mxnet as mx
import os

# Set device
ctx = mx.gpu() if mx.context.num_gpus() > 0 else mx.cpu()

# Define parameters
dataset_path = "dataset"
batch_size = 32
num_classes = len(os.listdir(dataset_path))  # Assuming each subdirectory represents a different person

# Data preprocessing
data_transforms = insightface.data.transforms.Compose([
    insightface.data.transforms.RandomHorizontalFlip(),
    insightface.data.transforms.RandomResizedCrop(size=(112, 112)),
    insightface.data.transforms.ToTensor(),
    insightface.data.transforms.Normalize(mean=0.5, std=0.5)
])

# Create data loader
train_dataset = insightface.data.FaceDataset(dataset_path, transform=data_transforms)
train_loader = mx.gluon.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# Define model
model = insightface.model_zoo.get_model('arcface_r100_v1', num_classes=num_classes, pretrained=False, ctx=ctx)
model.hybridize()

# Define loss function
criterion = insightface.loss.ArcFaceLoss(scale=64.0, margin=0.5)

# Define optimizer
optimizer = mx.gluon.Trainer(model.collect_params(), 'sgd', {'learning_rate': 0.1, 'wd': 5e-4})

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs = inputs.as_in_context(ctx)
        labels = labels.as_in_context(ctx)

        with mx.autograd.record():
            outputs = model(inputs)
            loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step(batch_size)

        running_loss += mx.nd.mean(loss).asscalar()
    
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss / len(train_loader)}")

# Save trained model
model.save_parameters("face_recognition_model.params")
