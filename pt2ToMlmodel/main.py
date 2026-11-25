import torch
import torchvision
from torchvision.models import MobileNet_V2_Weights
import coremltools as ct


def calculate_tensor_shape(tensor: torch.Tensor) -> tuple:
    if not hasattr(tensor, "shape"):
        raise AttributeError("Input does not have expected 'shape' attribute")
    return tuple(tensor.shape)


def convert_with_flags(
    model_to_convert,
    example_tensor: torch.Tensor,
    output_path: str = "coreMl.mlpackage",
) -> None:
    input_type = ct.TensorType(shape=calculate_tensor_shape(example_tensor))
    mlmodel = ct.convert(
        model_to_convert,
        inputs=[input_type],
    )
    print("[OK]\tmodel_from_trace coreML exported")
    mlmodel.save(output_path)


def main() -> None:
    torch_model = torchvision.models.mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
    torch_model.eval()
    example_input = (torch.rand(1, 3, 224, 224),)
    
    print(f"Exporting the model {torch_model.__class__.__name__}")
    traced_model = torch.jit.trace(torch_model, example_input)
    exported_program = torch.export.export(torch_model, example_input)
    torch.export.save(exported_program, "out_mod.pt2")
    convert_with_flags(traced_model, example_input[0])


if __name__ == "__main__":
    main()
