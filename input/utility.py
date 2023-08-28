import matplotlib
import matplotlib.pyplot as plt
import torch

matplotlib.style.use('ggplot')
def save_model(epochs, model, optimizer, criterion):
    torch.save({
        'epoch': epochs,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': criterion,
    }, f"../outputs/model.pth")

def save_plots(train_acc, valid_acc, train_loss, valid_loss):
    plt.figure(figsize=(10, 10))
    plt.plot(
        train_acc, color='black', linestyle='-', label='train accuracy'
    )
    plt.plot(
        valid_acc, color='blue', linestyle='-', label='validation accuracy'
    )
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.savefig(f"../outputs/accuracy.png")

    plt.figure(figsize=(10, 10))
    plt.plot(
        train_loss, color='green', linestyle='-', label='train loss'
    )

    plt.plot(
        valid_loss, color='yellow', linestyle='-', label = 'validation loss'
    )
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(f"../outputs/loss.png")