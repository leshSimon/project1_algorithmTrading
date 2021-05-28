# =============================================================================
# step23.py부터 step32.py까지는 simple_core를 이용해야 합니다.
is_simple_core = False  # True
# =============================================================================

if is_simple_core:
    from AI.dezero.core_simple import Variable
    from AI.dezero.core_simple import Function
    from AI.dezero.core_simple import using_config
    from AI.dezero.core_simple import no_grad
    from AI.dezero.core_simple import as_array
    from AI.dezero.core_simple import as_variable
    from AI.dezero.core_simple import setup_variable

else:
    from AI.dezero.core import Variable
    from AI.dezero.core import Parameter
    from AI.dezero.core import Function
    from AI.dezero.core import using_config
    from AI.dezero.core import no_grad
    from AI.dezero.core import test_mode
    from AI.dezero.core import as_array
    from AI.dezero.core import as_variable
    from AI.dezero.core import setup_variable
    from AI.dezero.core import Config
    from AI.dezero.layers import Layer
    from AI.dezero.models import Model
    from AI.dezero.datasets import Dataset
    from AI.dezero.dataloaders import DataLoader
    from AI.dezero.dataloaders import SeqDataLoader

    import AI.dezero.datasets
    import AI.dezero.dataloaders
    import AI.dezero.optimizers
    import AI.dezero.functions
    import AI.dezero.functions_conv
    import AI.dezero.layers
    import AI.dezero.utils
    import AI.dezero.cuda
    import AI.dezero.transforms

setup_variable()
__version__ = "0.0.13"
