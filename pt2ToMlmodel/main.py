import argparse

import torch
import torchvision
from torchvision.models import MobileNet_V2_Weights
import coremltools as ct

DEFAULT_INPUT = "out_mod.pt2"
DEFAULT_OUTPUT = "coreMl.mlpackage"


def calculate_tensor_shape(tensor: torch.Tensor) -> tuple:
    if not hasattr(tensor, "shape"):
        raise AttributeError("Input does not have expected 'shape' attribute")
    return tuple(tensor.shape)


def convert_with_flags(
    model_to_convert,
    example_tensor: torch.Tensor,
    output_path: str = DEFAULT_OUTPUT,
) -> None:
    input_type = ct.TensorType(shape=calculate_tensor_shape(example_tensor))
    mlmodel = ct.convert(
        model_to_convert,
        inputs=[input_type],
    )
    print("[OK]\tmodel_from_trace coreML exported")
    mlmodel.save(output_path)


def convert_exported(input_path: str, output_path: str) -> None:
    exported_program = torch.export.load(input_path).run_decompositions({})
    mlmodel = ct.convert(exported_program)
    print("[OK]\tmodel_from_pt2 coreML exported")
    mlmodel.save(output_path)


def build_mobilenet(input_path: str, output_path: str) -> None:
    torch_model = torchvision.models.mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
    torch_model.eval()
    example_input = (torch.rand(1, 3, 224, 224),)

    print(f"Exporting the model {torch_model.__class__.__name__}")
    traced_model = torch.jit.trace(torch_model, example_input)
    exported_program = torch.export.export(torch_model, example_input)
    torch.export.save(exported_program, input_path)
    convert_with_flags(traced_model, example_input[0], output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a torch.export .pt2 package to CoreML.")
    parser.add_argument(
        "--input",
        help=f"the .pt2 package to convert. Without it, MobileNetV2 is built and saved to {DEFAULT_INPUT} first",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"where the .mlpackage goes (default {DEFAULT_OUTPUT})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.input:
        convert_exported(args.input, args.output)
    else:
        build_mobilenet(DEFAULT_INPUT, args.output)


if __name__ == "__main__":
    main()
