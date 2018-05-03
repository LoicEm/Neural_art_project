import torch
from torch.autograd import Variable


import neural_transfer
from neural_transfer.net import Net, Vgg16


def neural_transform(content_image, style_image, output_image, style_size=256, content_size=256,
                     style_scale=None, cuda=False, model='model/'):
    """Copy of the eval function in main.py of the neural style module
        content_image : path to the content image
        content_size : width of the output image
        style_image : size of the style image
        style_size : width of the style image"""

    if style_scale is not None:
        style_size = content_size * style_scale

    content_image = neural_transfer.utils.tensor_load_rgbimage(content_image, size=content_size, keep_asp=True)
    content_image = content_image.unsqueeze(0)
    style = neural_transfer.utils.tensor_load_rgbimage(style_image, size=style_size)
    style = style.unsqueeze(0)
    style = neural_transfer.utils.preprocess_batch(style)

    style_model = Net(ngf=128)
    style_model.load_state_dict(torch.load(model), False)

    if cuda:
        style_model.cuda()
        content_image = content_image.cuda()
        style = style.cuda()

    style_v = Variable(style)

    content_image = Variable(neural_transfer.utils.preprocess_batch(content_image))
    style_model.setTarget(style_v)

    output = style_model(content_image)
    neural_transfer.utils.tensor_save_bgrimage(output.data[0], output_image, cuda)
    return(output_image)
