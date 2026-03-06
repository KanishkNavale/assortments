import torch


def is_rotationmatrix(
    rotation_matrix: torch.Tensor,
    tolerance: float = 1e-3,
) -> bool:
    R = rotation_matrix.clone()
    E = torch.eye(3, device=R.device, dtype=rotation_matrix.dtype)
    determinant_R = torch.linalg.det(R)

    return torch.allclose(
        R.T @ R,
        E,
        atol=tolerance,
    ) and torch.allclose(
        determinant_R,
        torch.ones_like(determinant_R),
        atol=tolerance,
    )
