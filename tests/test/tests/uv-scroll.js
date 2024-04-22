const fs = require('fs');
const path = require('path')
const assert = require('assert');
const utils = require('../utils.js');

module.exports = {
    description: 'can export uv-scroll',
    test: outDirPath => {
        let gltfPath = path.resolve(outDirPath, 'uv-scroll.gltf');
        const asset = JSON.parse(fs.readFileSync(gltfPath));

        assert.strictEqual(asset.extensionsUsed.includes('MOZ_hubs_components'), true);
        assert.strictEqual(utils.checkExtensionAdded(asset, 'MOZ_hubs_components'), true);

        const node = asset.nodes[0];
        assert.strictEqual(utils.checkExtensionAdded(node, 'MOZ_hubs_components'), true);

        const ext = node.extensions['MOZ_hubs_components'];
        assert.deepStrictEqual(ext, {
            "uv-scroll": {
                "speed": {
                    "x": 0,
                    "y": 0
                },
                "increment": {
                    "x": 0,
                    "y": 0
                }
            }
        });
    }
};