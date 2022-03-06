import torch
from app.services.model import BiSeNet
from PIL import Image
import torchvision.transforms as transforms


def evaluate(image_path, cp="./app/data/models/79999_iter.pth"):
    n_classes = 19
    net = BiSeNet(n_classes=n_classes).to("cpu")

    net.load_state_dict(torch.load(cp, map_location=torch.device("cpu")))
    net.eval()

    to_tensor = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ]
    )

    with torch.no_grad():
        img = Image.open(image_path)
        image = img.resize((512, 512), Image.BILINEAR)
        img = to_tensor(image)
        img = torch.unsqueeze(img, 0)
        out = net(img)[0]
        parsing = out.squeeze(0).cpu().numpy().argmax(0)

        return parsing
