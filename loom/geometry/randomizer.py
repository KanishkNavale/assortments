import torch


def generate_random_so3(batch_size: int = 1) -> torch.Tensor:
    random_matrix = torch.rand(batch_size, 3, 3)

    centered = random_matrix - torch.mean(random_matrix, dim=-1, keepdim=True)
    U, _, VT = torch.linalg.svd(centered)
    V = VT.permute(0, 2, 1)

    # Handling reflection case!
    normalizer = torch.eye(3).unsqueeze(0).repeat(batch_size, 1, 1)
    normalizer[:, -1, -1] = torch.linalg.det(V @ U.permute(0, 2, 1))

    return V @ normalizer.detach() @ U.permute(0, 2, 1)
