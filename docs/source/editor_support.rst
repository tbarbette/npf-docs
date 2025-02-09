.. _editor_support:

*************************
Editor support
*************************

NPF support in editors and IDEs is currently WIP. Support for syntax highlighting is available through a `Tree-sitter <https://tree-sitter.github.io/tree-sitter/>`_ parser, available `here <https://github.com/ntyunyayev/tree-sitter-npf>`_. 

Supported editors
========

Even if not in the list, all editors using Tree-sitter should be compatible with the parser. Currently, VSCode is not supported as it does not use Tree-sitter by default, but you can have a look at `Zed <https://github.com/zed-industries/zed>`_ (instructions below) which is fairly similar and has VSCode key binding. The following tutorial assumes that you are using Linux.

Neovim
--------

To get started with using NPF with `Neovim <https://github.com/neovim/neovim>`_, a small config file is `available <https://github.com/ntyunyayev/nvim-npf-config>`_. The **init.lua** file should be put at ~/.config/nvim/init.lua. This is a small config aimed at people that want to quickly edit NPF file through Neovim and want a simple config that just works.

If you are already familiar with Neovim and already have a Neovim config, you can replace the **nvim-treesitter/nvim-treesitter** plugin by the forked supporting NPF : **ntyunyayev/nvim-treesitter**:

..  code-block:: lua

    {
        -- Highlight, edit, and navigate code
        'ntyunyayev/nvim-treesitter',
        dependencies = {
            'nvim-treesitter/nvim-treesitter-textobjects',
        },
        build = ':TSUpdate',
    },

Then you can install the NPF parser from inside Neovim:

..  code-block:: interactive

    :TSInstall npf

Helix
--------

For `Helix <https://github.com/helix-editor/helix>`_ users, a small config is also available `here <https://github.com/ntyunyayev/helix-npf>`_. You can copy the content inside **~/.config/helix**.

Zed
--------

If you come from VSCode, this option will be the most familiar for your. An extension is available `here <https://github.com/ntyunyayev/zed-npf>`_. You can simply clone the repo and then open Zed, open the extensions menu (CTRL+SHIFT+X) click on **Install Dev Extension** and search for the cloned repo.


